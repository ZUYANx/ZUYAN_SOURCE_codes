import requests
import time
import json
import sqlite3
import rich
import time
import os
from rich.live import Live
from rich import print
from rich.panel import Panel
from rich.console import Console
# Setup SQLite connection (adjust path or db as needed)
conn = sqlite3.connect('history.db')
cursor = conn.cursor()
session = requests.Session()
console = Console()
cursor.execute('''
CREATE TABLE IF NOT EXISTS history (
    issue_number TEXT PRIMARY KEY,
    number TEXT,
    color TEXT
)
''')
conn.commit()
#======[colour]=======#
R = "[red]"
O = "[orange]"
Y = "[yellow]"
G = "[green]"
B = "[blue]"
I = "[indigo]"
V = "[violet]"
P = "[purple]"
C = "[cyan]"
M = "[magenta]"
W = "[white]"
#================#
def save_history_to_db(server_list):
    # Save new server history to local DB (upsert)
    for item in server_list:
        issue = item.get('issueNumber')
        number = item.get('number')
        color = item.get('color')
        if issue and number:
            cursor.execute('''
            INSERT OR REPLACE INTO history(issue_number, number, color)
            VALUES (?, ?, ?)
            ''', (issue, number, color))
    conn.commit()

def get_token():
    head = {
        "accept": "*/*",
        "origin": "https://dkwin9.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
        "referer": "https://dkwin9.com/",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json"
    }
    data = {
        "username": "8801976145468",
        "pwd": "zuyan123",
        "phonetype": 1,
        "logintype": "mobile",
        "language": 0,
        "random": "f121ddd0cf20443abad4613079fc7cd6",
        "signature": "F14225FC3D3370917BEBB8ECF706A0F3",
        "timestamp": int(time.time())
    }
    login = session.post("https://api.dkwinapi.com/api/webapi/Login", headers=head, json=data)
    if login.status_code == 200 and login.json().get('data'):
        print("Login successful")
        return login.json()
    else:
        print("Login failed or skipped.")
        return None

def get_local_history(last_n=20):
    cursor.execute('''
        SELECT issue_number, number, color FROM history ORDER BY issue_number DESC LIMIT ?
    ''', (last_n,))
    rows = cursor.fetchall()
    local_list = [{'issueNumber': row[0], 'number': row[1], 'color': row[2]} for row in rows]
    return local_list

def merge_histories(server_list, local_list):
    server_dict = {item['issueNumber']: item for item in server_list if 'issueNumber' in item}
    merged = list(server_list)
    for item in local_list:
        issue = item.get('issueNumber') or item.get('issue_number')
        if issue not in server_dict:
            merged.append(item)
    merged.sort(key=lambda x: x.get('issueNumber') or x.get('issue_number'), reverse=True)
    return merged

def get_history():
    head = {
        "accept": "*/*",
        "origin": "https://dkwin9.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
        "referer": "https://dkwin9.com/",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json"
    }
    try:
        response = session.get("https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json", headers=head)
        response.raise_for_status()
        server_data = response.json()
        server_list = server_data.get('data', {}).get('list', [])
        local_list = get_local_history(last_n=20)
        merged_list = merge_histories(server_list, local_list)
        save_history_to_db(server_list)
        return {'data': {'list': merged_list}}
    except Exception as e:
        print("Failed to fetch server history:", e)
        local_list = get_local_history(last_n=20)
        return {'data': {'list': local_list}}

def get_time():
    head = {
        "accept": "*/*",
        "origin": "https://dkwin9.com",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
        "referer": "https://dkwin9.com/",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json"
    }
    try:
        response = session.get("https://draw.ar-lottery01.com/WinGo/WinGo_30S.json", headers=head, timeout=5)
        response.raise_for_status()
        data = response.json()
        next_data = data.get("next", {})
        start_time_ms = next_data.get("startTime")
        issue_number = next_data.get("issueNumber")
        end_time_ms = next_data.get("endTime")
        if start_time_ms and issue_number and end_time_ms:
            return start_time_ms // 1000, issue_number, end_time_ms // 1000
        else:
            return None, None, None
    except Exception as e:
        print("Failed to fetch time info:", e)
        return None, None, None

def analyze_history(history):
    try:
        rounds = history['data']['list'][:50]
        numbers = [int(r['number']) for r in rounds]
        colors = [r.get('color', 'unknown') for r in rounds]
        
        if len(numbers) < 7:
            return {'number_pred': 4, 'big': False, 'small': True, 'common_colors': ['red']}
        
        # PATTERN MASTER - Ultra Deep Analysis
        
        last_2 = numbers[:2]
        last_3 = numbers[:3]
        last_5 = numbers[:5]
        last_7 = numbers[:7]
        last_10 = numbers[:10]
        
        prediction = None
        master_thinking = ""
        pattern_strength = 0
        
        # LEVEL 1: SEQUENCE PATTERN MASTER
        # Check for mathematical sequences
        if len(last_3) == 3:
            diff1 = last_3[1] - last_3[0]
            diff2 = last_3[2] - last_3[1]
            
            # Arithmetic sequence (constant difference)
            if diff1 == diff2 and diff1 != 0:
                next_in_seq = last_3[2] + diff1
                if 0 <= next_in_seq <= 9:
                    prediction = next_in_seq
                    master_thinking = f"arithmetic_sequence_+{diff1}"
                    pattern_strength = 9
                else:
                    # Sequence breaks boundary, reverse it
                    prediction = 9 - last_3[2] if last_3[2] < 5 else last_3[2] - 9
                    if prediction < 0: prediction = abs(prediction)
                    master_thinking = "sequence_boundary_break"
                    pattern_strength = 8
        
        # LEVEL 2: CYCLE PATTERN MASTER  
        if prediction is None:
            # Look for repeating cycles of different lengths
            for cycle_len in range(2, 8):
                if len(numbers) >= cycle_len * 3:  # Need at least 3 full cycles
                    cycle_matches = 0
                    cycle_total = 0
                    
                    # Check how well the cycle repeats
                    for i in range(cycle_len, len(numbers)):
                        if numbers[i] == numbers[i % cycle_len]:
                            cycle_matches += 1
                        cycle_total += 1
                    
                    cycle_accuracy = cycle_matches / cycle_total if cycle_total > 0 else 0
                    
                    # If cycle is strong (>70% accuracy)
                    if cycle_accuracy > 0.7:
                        next_pos = len(numbers) % cycle_len
                        if next_pos < len(numbers):
                            prediction = numbers[next_pos]
                            master_thinking = f"cycle_{cycle_len}_accuracy_{int(cycle_accuracy*100)}%"
                            pattern_strength = int(cycle_accuracy * 10)
                            break
        
        # LEVEL 3: MIRROR PATTERN MASTER
        if prediction is None:
            # Check for mirror/reflection patterns
            if len(last_5) == 5:
                # Check if pattern mirrors around center
                if last_5[0] == last_5[4] and last_5[1] == last_5[3]:
                    # Perfect mirror, continue pattern
                    prediction = last_5[1]  # Mirror the second position
                    master_thinking = "mirror_pattern_perfect"
                    pattern_strength = 8
                # Partial mirror
                elif last_5[0] == last_5[3] or last_5[1] == last_5[4]:
                    # Partial mirror detected
                    prediction = 9 - last_5[0]  # Inverse mirror
                    if prediction < 0 or prediction > 9:
                        prediction = last_5[2]
                    master_thinking = "mirror_pattern_partial"
                    pattern_strength = 6
        
        # LEVEL 4: FIBONACCI-LIKE PATTERN MASTER
        if prediction is None and len(last_3) == 3:
            # Check if numbers follow fibonacci-like pattern
            if last_3[2] == (last_3[0] + last_3[1]) % 10:
                # Fibonacci pattern detected
                next_fib = (last_3[1] + last_3[2]) % 10
                prediction = next_fib
                master_thinking = "fibonacci_pattern"
                pattern_strength = 7
            elif last_3[2] == abs(last_3[0] - last_3[1]):
                # Difference pattern detected
                next_diff = abs(last_3[1] - last_3[2])
                prediction = next_diff
                master_thinking = "difference_pattern"
                pattern_strength = 7
        
        # LEVEL 5: BIG/SMALL WAVE PATTERN MASTER
        if prediction is None:
            # Analyze big/small waves with precision
            wave_pattern = []
            for num in last_7:
                wave_pattern.append('B' if num >= 5 else 'S')
            
            # Look for repeating wave patterns
            wave_str = ''.join(wave_pattern)
            
            # Common wave patterns
            if 'BSBSBS' in wave_str:  # Perfect alternating
                last_was_big = wave_pattern[0] == 'B'
                prediction = 2 if last_was_big else 7
                master_thinking = "perfect_wave_alternating"
                pattern_strength = 9
            elif 'BBSSBB' in wave_str or 'SSBBS' in wave_str:  # Double wave
                if wave_pattern[0] == wave_pattern[1]:  # Double same, switch
                    prediction = 2 if wave_pattern[0] == 'B' else 7
                    master_thinking = "double_wave_break"
                    pattern_strength = 8
                else:
                    prediction = 7 if wave_pattern[0] == 'S' else 2
                    master_thinking = "double_wave_continue"
                    pattern_strength = 7
            elif wave_pattern[:3] == ['B','B','B'] or wave_pattern[:3] == ['S','S','S']:
                # Triple domination - STRONG break needed
                prediction = 1 if wave_pattern[0] == 'B' else 8
                master_thinking = "triple_domination_break"
                pattern_strength = 9
        
        # LEVEL 6: GHOST NUMBER HUNTING MASTER
        if prediction is None:
            # Advanced ghost analysis with scoring
            ghost_scores = {}
            
            # Analyze absence patterns for each number
            for target_num in range(10):
                last_seen = -1
                for i, num in enumerate(numbers):
                    if num == target_num:
                        last_seen = i
                        break
                
                if last_seen == -1:  # Never seen in history
                    ghost_scores[target_num] = 50  # Maximum ghost score
                elif last_seen >= 15:  # Not seen in last 15
                    ghost_scores[target_num] = 30
                elif last_seen >= 10:  # Not seen in last 10
                    ghost_scores[target_num] = 20
                elif last_seen >= 7:   # Not seen in last 7
                    ghost_scores[target_num] = 15
                else:
                    ghost_scores[target_num] = 0
            
            # Find the most ghost number
            if ghost_scores:
                ghost_num = max(ghost_scores, key=ghost_scores.get)
                if ghost_scores[ghost_num] >= 15:
                    prediction = ghost_num
                    master_thinking = f"ghost_hunting_score_{ghost_scores[ghost_num]}"
                    pattern_strength = min(9, ghost_scores[ghost_num] // 5)
        
        # LEVEL 7: LAST RESORT MASTER LOGIC
        if prediction is None:
            # Use advanced last resort logic
            last_num = numbers[0]
            
            # Count frequency in different windows
            freq_3 = {}
            freq_7 = {}
            for num in last_3:
                freq_3[num] = freq_3.get(num, 0) + 1
            for num in last_7:
                freq_7[num] = freq_7.get(num, 0) + 1
            
            # If a number dominates recent history, break it
            if freq_3:
                dominant_num = max(freq_3, key=freq_3.get)
                if freq_3[dominant_num] >= 2:  # Appeared 2+ times in last 3
                    # Pick opposite range number that's least frequent
                    opposite_range = range(0, 5) if dominant_num >= 5 else range(5, 10)
                    opposite_freqs = {n: freq_7.get(n, 0) for n in opposite_range}
                    prediction = min(opposite_freqs, key=opposite_freqs.get)
                    master_thinking = "dominant_break_opposite"
                    pattern_strength = 6
                else:
                    # No clear dominance, use balance logic
                    prediction = 5 - last_num if last_num < 5 else 14 - last_num
                    master_thinking = "balance_logic"
                    pattern_strength = 4
        
        # COLOR PATTERN MASTER ANALYSIS
        color_pred = []
        color_thinking = ""
        color_strength = 0
        
        if len(colors) >= 5:
            last_5_colors = colors[:5]
            
            # Level 1: Triple streak break
            if colors[0] == colors[1] == colors[2]:
                # Triple streak - BREAK IT!
                if colors[0] == 'red':
                    color_pred = ['green']
                    color_thinking = "triple_red_break"
                    color_strength = 9
                elif colors[0] == 'green':  
                    color_pred = ['violet']
                    color_thinking = "triple_green_break"
                    color_strength = 9
                else:
                    color_pred = ['red']
                    color_thinking = "triple_violet_break"
                    color_strength = 9
            
            # Level 2: Alternating color pattern
            elif len(set(colors[:4])) == 2 and colors[0] != colors[1]:
                # Alternating detected
                if colors[0] == colors[2]:
                    color_pred = [colors[1]]  # Continue alternating
                    color_thinking = "alternating_continue"
                    color_strength = 8
                else:
                    color_pred = [colors[0]]  # Return to first color
                    color_thinking = "alternating_return"
                    color_strength = 7
            
            # Level 3: Color ghost hunting
            else:
                color_last_seen = {}
                for color in ['red', 'green', 'violet']:
                    for i, c in enumerate(colors):
                        if c == color:
                            color_last_seen[color] = i
                            break
                    if color not in color_last_seen:
                        color_last_seen[color] = 99  # Never seen
                
                # Pick most ghost color
                ghost_color = max(color_last_seen, key=color_last_seen.get)
                color_pred = [ghost_color]
                color_thinking = f"{ghost_color}_ghost_hunt"
                color_strength = min(8, color_last_seen[ghost_color])
        else:
            color_pred = ['green']
            color_thinking = "default_green"
            color_strength = 3
        
        # MASTER CONFIDENCE CALCULATION
        total_confidence = pattern_strength + color_strength
        if total_confidence >= 16:
            master_confidence = "PATTERN MASTER"
        elif total_confidence >= 12:
            master_confidence = "EXPERT"
        elif total_confidence >= 8:
            master_confidence = "ADVANCED"
        else:
            master_confidence = "STANDARD"
        
        return {
            'number_pred': prediction if prediction is not None else 5,
            'big': (prediction if prediction is not None else 5) >= 5,
            'small': (prediction if prediction is not None else 5) < 5,
            'common_colors': color_pred,
            'pattern_master_analysis': {
                'thinking': master_thinking,
                'pattern_strength': pattern_strength,
                'color_thinking': color_thinking,
                'color_strength': color_strength,
                'master_confidence': master_confidence,
                'total_score': total_confidence,
                'analysis_levels': 7
            }
        }
        
    except Exception as e:
        return {
            'number_pred': 3,
            'big': False,
            'small': True,
            'common_colors': ['red'],
            'error': 'pattern_master_fallback'
        }
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        #token = get_token()  # Login first
       # if not token:
         #   print(Panel(f"{R}Could not login, continuing without login...", title="ERROR", border_style="bold green"))
        while True:  # infinite loop to repeat rounds
            clear_screen()
            history = get_history()
            start_time, issue_number, end_time = get_time()
            if not start_time:
                print(Panel(f"{R}Failed to fetch start time, retrying in 5 seconds...", border_style="bold green", title="ERROR"))
                time.sleep(5)
                continue  
            analysis = analyze_history(history)
            print(Panel.fit(f"{G}Round {issue_number} started!", border_style="bold green", title="ISSUE-NUMBER"))
            print(Panel.fit(f"{G}Number prediction: {analysis['number_pred']} (Big: {analysis['big']}, Small: {analysis['small']})", border_style="bold green", title="PREDICTIONS"))
            print(Panel.fit(f"{G}Most common color(s): {', '.join(analysis['common_colors'])}", border_style="bold green", title="COLOURS"))
            with Live(refresh_per_second=4) as live:
                while int(time.time()) < start_time:
                    wait_sec = start_time - int(time.time())
                    live.update(Panel(f"Waiting to start: {wait_sec} sec", border_style="bold yellow", title="Countdown"))
                    time.sleep(0.25)
    except Exception as e:
        print(Panel.fit(f"  {R}NO INTERNET or ERROR: {e}", border_style="bold red"))








if __name__ == "__main__":
    main()
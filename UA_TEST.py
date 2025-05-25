import random

def ua():
    fb_versions = [
        "335.0.0.28.118", "336.0.0.30.62", "337.1.0.29.120", "338.0.0.32.110"
    ]
    languages = [
        "en_US", "en_GB", "ru_RU", "hi_IN", "id_ID", "es_ES"
    ]
    carriers = [
        "Bezlimit", "T-Mobile", "AT&T", "Banglalink", "Grameenphone", "Vodafone"
    ]
    brands = [
        ("Xiaomi", "Redmi Note 8 Pro"),
        ("Samsung", "Galaxy S10"),
        ("Realme", "Realme 5 Pro"),
        ("Huawei", "P30 Lite"),
        ("OnePlus", "OnePlus 7T"),
        ("Oppo", "A5 2020"),
        ("Vivo", "Vivo Y20")
    ]
    densities = [2.0, 2.5, 2.75, 3.0, 3.5]
    width_height = [
        (1080, 2220),
        (720, 1520),
        (1080, 2400),
        (1080, 2340)
    ]
    cpu_archs = [
        "armeabi-v7a:armeabi", "arm64-v8a", "x86_64"
    ]

    fbav = random.choice(fb_versions)
    fbpn = "com.facebook.katana"
    fblc = random.choice(languages)
    fbbv = str(random.randint(300000000, 400000000))
    fbcr = random.choice(carriers)
    fbmf, fbbd = random.choice(brands)
    fbdv = fbbd
    fbsv = random.choice(["10", "11", "12", "13"])
    fbca = random.choice(cpu_archs)
    width, height = random.choice(width_height)   # <-- only width and height
    density = random.choice(densities)             # <-- density separately
    fb_fw = "1"
    fbrv = str(random.randint(300000000, 400000000))

    u = (f"FBAN/FB4A;FBAV/{fbav};FBPN/{fbpn};FBLC/{fblc};FBBV/{fbbv};"
         f"FBCR/{fbcr};FBMF/{fbmf};FBBD/{fbbd};FBDV/{fbdv};FBSV/{fbsv};"
         f"FBCA/{fbca};FBDM={{density={density},width={width},height={height}}};"
         f"FB_FW/{fb_fw};FBRV/{fbrv};]")
    
    return u
    
print(ua())
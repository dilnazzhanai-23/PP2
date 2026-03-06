import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

prices = re.findall(r"\d[\d ]*,\d{2}", text)

products = re.findall(r"\d+\.\n(.+)", text)

total = sum(float(p.replace(" ", "").replace(",", ".")) for p in prices)

datetime = re.search(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}", text)
datetime = datetime.group() if datetime else None

payment = "Банковская карта" if re.search(r"Банковская карта", text) else "Другой"

data = {
    "products": products,
    "prices": prices,
    "total": total,
    "datetime": datetime,
    "payment": payment
}


print(json.dumps(data, ensure_ascii=False, indent=2))
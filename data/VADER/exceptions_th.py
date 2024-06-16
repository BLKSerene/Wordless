NEGATE = ['ไม่', 'ใช่', 'อยู่', 'ได้', 'สามารถ', 'ทำ', 'กล้า', 'อย่า', 'อาจ', 'ต้อง', 'ทั้งสอง', 'อย่าง', 'อาจจะ', 'จะ', 'จำเป็น', 'เคย', 'มี', 'ก็', 'เช่นกัน', 'อะไร', 'ที่ไหน', 'เลย', 'ควร', 'ชานต์', 'เอ่อ', 'ปราศจาก', 'คง', 'นานๆ ครั้ง', 'ไม่ค่อย', 'ถึงอย่างไรก็ตาม']
BOOSTER_DICT = {'อย่าง': 0.293, 'แน่นอน': 0.293, 'น่าอัศจรรย์': 0.293, 'มาก': 0.293, 'สมบูรณ์': 0.293, 'เด็ดเดี่ยว': 0.293, 'ลึกซึ้ง': 0.293, 'เอฟ': 0.293, 'ฟิง': 0.293, 'มหาศาล': 0.293, 'โดยสิ้นเชิง': 0.293, 'โดยเฉพาะ': 0.293, 'พิเศษ': 0.293, 'เป็นพิเศษ': 0.293, 'สุดขีด': 0.293, 'ที่สุด': 0.293, 'เยี่ยมยอด': 0.293, 'พลิก': 0.293, 'พิน': 0.293, 'แฟรกคิน': 0.293, 'แฟร็กกิ้ง': 0.293, 'สะบัด': 0.293, 'ฟ': 0.293, 'ริก': 0.293, 'กิ้น': 0.293, 'การ': 0.293, 'แช่เย็น': 0.293, 'กิน': 0.293, 'เต็มที่': 0.293, 'ไอ้': 0.293, 'เหี้ย': 0.293, 'โคตร': 0.293, 'ๆ': 0.293, 'คน': 0.293, 'ขี้โกง': 0.293, 'โกหก': 0.293, 'เฮ': 0.293, 'ล': 0.293, 'ลา': 0.293, 'สูง': 0.293, 'เหลือเชื่อ': 0.293, 'เข้มข้น': 0.293, 'วิชาเอก': 0.293, 'สำคัญ': 0.293, 'มากกว่า': 0.293, 'หมดจด': 0.293, 'ค่อนข้าง': -0.293, 'จริง': 0.293, 'หรือ': 0.293, 'น่าทึ่ง': 0.293, 'ดังนั้น': 0.293, 'มี': 0.293, 'นัยสำคัญ': 0.293, 'ละเอียด': 0.293, 'ทั้งหมด': 0.293, 'อู': 0.293, 'เบอร์': 0.293, 'ไม่': -0.293, 'น่าเชื่อ': 0.293, 'ผิดปกติ': 0.293, 'เกือบ': -0.293, 'แทบจะ': -0.293, 'แค่': -0.293, 'เพียงพอ': -0.293, 'ชนิด': -0.293, 'ของ': -0.293, 'เล็กน้อย': -0.293, 'น้อย': -0.293, 'ร่อแร่': -0.293, 'เป็นครั้งคราว': -0.293, 'บางส่วน': -0.293, 'ขาดแคลน': -0.293, 'เรียงลำดับ': -0.293}
SENTIMENT_LADEN_IDIOMS = {'ตัด มัสตาร์ด': 2.0, 'มือ ต่อปาก': -2.0, 'ส่งคืน': -2.0, 'เป่า ควัน': -2.0, 'ยก มือขึ้น': 1.0, 'ขา หัก': 2.0, 'การปรุงอาหาร ด้วย แก๊ส': 2.0, 'ใน สี ดำ': 2.0, 'ใน สีแดง': -2.0, 'บน ลูกบอล': 2.0, 'ภายใต้ สภาพอากาศ': -2.0}
SPECIAL_CASES = {'อึ': 3.0, 'ระเบิด': 3.0, 'ลา ไม่ ดี': 1.5, 'ไอ้ เหี้ย': 1.5, 'ป้ายรถเมล์': 0.0, 'ช่าย ยย': -2.0, 'จูบ มรณะ': -1.5, 'ที่จะ ตาย เพื่อ': 3.0, 'หัว ใจเต้น': 3.5}
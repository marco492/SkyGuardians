from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import black, darkblue
from datetime import datetime
import os

def create_cathay_delay_certificate(flight_data_index=0):
    # 三個硬編碼的航班延遲信息範例
    flight_data_options = [
        {
            'flight_number': 'CX451',
            'delay_date': '15 NOV 2023',
            'departure': 'Hong Kong (HKG)',
            'destination': 'Taipei (TPE)',
            'original_flight': 'CX451 / 14:25',
            'actual_flight': 'CX451 / 17:45',
            'delay_reason': 'Technical issue with aircraft requiring maintenance check',
            'delay_time': '3 hours 20 minutes',
            'customer_name': 'CHEN WEI-LIN',
            'reservation_code': 'CX8K9P2',
            'issue_date': datetime.now().strftime('%d %b %Y')
        },
        {
            'flight_number': 'CX712',
            'delay_date': '18 NOV 2023',
            'departure': 'Tokyo (NRT)',
            'destination': 'Hong Kong (HKG)',
            'original_flight': 'CX712 / 09:30',
            'actual_flight': 'CX712 / 11:15',
            'delay_reason': 'Air traffic control restrictions',
            'delay_time': '1 hour 45 minutes',
            'customer_name': 'WONG TAK-MING',
            'reservation_code': 'CX3J7F1',
            'issue_date': datetime.now().strftime('%d %b %Y')
        },
        {
            'flight_number': 'CX831',
            'delay_date': '20 NOV 2023',
            'departure': 'Hong Kong (HKG)',
            'destination': 'London (LHR)',
            'original_flight': 'CX831 / 23:15',
            'actual_flight': 'CX831A / 02:30',
            'delay_reason': 'Crew scheduling issue due to previous flight delay',
            'delay_time': '3 hours 15 minutes',
            'customer_name': 'SMITH JOHN',
            'reservation_code': 'CX5M2K9',
            'issue_date': datetime.now().strftime('%d %b %Y')
        }
    ]
    
    # 選擇要使用的航班數據
    selected_data = flight_data_options[flight_data_index]
    
    # 生成PDF
    generate_flight_certificate_pdf(selected_data)

def generate_flight_certificate_pdf(data):
    # 創建PDF文件
    pdf_filename = f"Cathay_Delay_Certificate_{data['reservation_code']}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    
    # 設置起始位置
    y_position = height - 50
    
    # 右上角航空商標 - 使用圖片
    # 請將 'cathay_logo.png' 替換為您的實際圖片路徑
    logo_path = 'cathay-pacific-logo-png_seeklogo-312434.png'
    try:
        if os.path.exists(logo_path):
            logo = ImageReader(logo_path)
            # 調整圖片大小和位置
            c.drawImage(logo, width - 250, y_position - 60, width=300, height=150, preserveAspectRatio=True)
        else:
            # 如果圖片不存在，使用文字作為備用
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(darkblue)
            c.drawRightString(width - 50, y_position, "CATHAY PACIFIC")
    except Exception as e:
        print(f"Error loading logo: {e}")
        # 如果載入圖片出錯，使用文字作為備用
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(darkblue)
        c.drawRightString(width - 50, y_position, "CATHAY PACIFIC")
    
    y_position -= 80
    
    # 標題 - 置中對齊
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(black)
    c.drawCentredString(width / 2, y_position, "Flight Delay Certificate")
    y_position -= 40
    
    # 上款
    c.setFont("Helvetica", 12)
    c.drawString(50, y_position, "To Whom It May Concern,")
    y_position -= 30
    
    # 航班信息
    c.setFont("Helvetica", 11)
    flight_info = [
        f"Flight Number: {data['flight_number']}",
        f"Date: {data['delay_date']}",
        f"From: {data['departure']}",
        f"To: {data['destination']}",
        f"Original flight number/time: {data['original_flight']}",
        f"Actual changed flight number/time: {data['actual_flight']}",
        f"Delay Reason: {data['delay_reason']}",
        f"Delay time: {data['delay_time']}",
        f"Customer Name: {data['customer_name']}",
        f"Reservation Code: {data['reservation_code']}"
    ]
    
    for info in flight_info:
        c.drawString(50, y_position, info)
        y_position -= 20
    
    y_position -= 20
    
    # 道歉語
    c.drawString(50, y_position, "We sincerely apologize for any inconvenience caused.")
    y_position -= 30
    
    # 航空公司簽名和日期
    c.drawString(50, y_position, "Cathay Pacific Airways")
    y_position -= 20
    c.drawString(50, y_position, data['issue_date'])
    y_position -= 40
    
    # 法律免責聲明
    disclaimer_text = [
        "This certificate will only be used by our Passenger for his/her personal insurance claims / hotel refund purposes. No person",
        "shall use this certificate for any ticket change or refund. The issuance of this certification shall not be construed as a waiver",
        "of any right or privilege of our company nor shall construe that the Company shall assume any responsibility to the Passenger."
    ]
    
    c.setFont("Helvetica-Bold", 8)
    for line in disclaimer_text:
        c.drawString(50, y_position, line)
        y_position -= 14
    
    # 保存PDF
    c.save()
    print(f"PDF certificate generated: {pdf_filename}")

def main():
    print("Generating Cathay Pacific Flight Delay Certificate...")
    print("Available flight delay options:")
    print("0: CX451 - Hong Kong to Taipei (3h 20m delay)")
    print("1: CX712 - Tokyo to Hong Kong (1h 45m delay)")
    print("2: CX831 - Hong Kong to London (3h 15m delay)")
    
    try:
        selection = int(input("Please select a flight delay option (0-2): "))
        if selection < 0 or selection > 2:
            print("Invalid selection. Using default option (0).")
            selection = 0
    except:
        print("Invalid input. Using default option (0).")
        selection = 0
    
    create_cathay_delay_certificate(selection)
    print("Certificate generation completed!")

if __name__ == "__main__":
    main()
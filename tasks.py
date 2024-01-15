from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
import time
from RPA.PDF import PDF
from RPA.Tables import Tables
from RPA.Archive import Archive


@task
def order_processing():
    """
    this is how you write 
    multiple line comments
    """


    open_robot_order_website()
    download_input_file()
    orders = read_csv_file()
    for order in orders:
        capture_order(order)
    zip_files()




def open_robot_order_website():
    #open browser and navigate to robot_spare_bin, and log into the app
    browser.configure(browser_engine="chrome",slowmo=100)
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    time.sleep(2)

def download_input_file():
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv",target_file="input.csv", overwrite=True)   

def read_csv_file():
    table=Tables()
    orders=table.read_table_from_csv("input.csv",header=True)
    return orders



def capture_order(order):
    print(order)
    order_number = (order["Order number"])
    page=browser.page()
    page.click(".btn.btn-dark")
    page.select_option("#head", str(order["Head"]))
    page.fill("#address", order["Address"])
    page.fill(".mb-3:nth-child(3) input", order["Legs"])
    page.click("#id-body-" + order["Body"])
    page.click("#preview")
    time.sleep(2)
    preview_img = browser.page().locator('id=robot-preview-image')
    preview_img.screenshot(path=f'output/imgs/img{order_number}.png')


    order_btn_exist = browser.page().locator('id=order').is_visible()
    
    while order_btn_exist == True:
        print(str(order_btn_exist))
        page.click("#order")
        order_btn_exist = browser.page().locator('id=order').is_visible()

    



    order_details_html = browser.page().locator('id=receipt').inner_html()
    pdf=PDF()
    pdf.html_to_pdf(order_details_html,f"output/receipts/{order_number}.pdf")

    #browser.screenshot("robot-preview-image", path="output/test.png")
    #page.screenshot(se)
    #page.click("#order")
    pdf.add_files_to_pdf(
        files=[f"output/imgs/img{order_number}.png"],
        target_document=f"output/receipts/{order_number}.pdf", append=True
    )
    
    page.click("#order-another")





    

def zip_files():
    archive = Archive()
    archive.archive_folder_with_zip("output/receipts", "output/receipts.zip")

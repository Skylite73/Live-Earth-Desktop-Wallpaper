import ctypes
from glob import glob
import os
from selenium.webdriver import Firefox, ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time


def get_latest_image(dir, filetype='.png'):
    candidate_images = glob(dir + r"\*" + filetype)
    if candidate_images:
        return max(candidate_images, key=os.path.getctime)
    else: 
        return

def move_image(image_path, new_dir):
    def recursive_rename_check(path):
        if os.path.exists(path):
            path = os.path.join(os.path.dirname(path), os.path.basename(path)[:-4] + "_Copy" + os.path.basename(path)[-4:])
            return recursive_rename_check(path)
        return path
    new_image_path = recursive_rename_check(os.path.join(new_dir, os.path.basename(image_path)))
    os.rename(image_path, new_image_path)
    return new_image_path
    
def set_desktop_background(image_path):
    print("Setting desktop background to: " + image_path)
    SPI_SETDESKWALLPAPER = 20
    SPIF_SENDCHANGE = 0#2
    SPIF_UPDATEINIFILE = 0#1
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, SPIF_SENDCHANGE, image_path, SPIF_UPDATEINIFILE)
    print("All done. Exiting...")

def download_satellite_image(resolution, slider_url):
    print("Starting up headless browser...")
    options = Options()
    options.page_load_strategy = 'eager'
    options.add_argument('-headless')
    driver = Firefox(options=options)
    driver.set_window_size(resolution[0],resolution[1]+45+40) # 45px header + 40px otherwise it breaks :/
    driver.implicitly_wait(60)
    driver.get(slider_url)
    
    print("Waiting 5s for page data to load...")
    
    ActionChains(driver)\
        .pause(5)\
        .send_keys("h")\
        .pause(0.2)\
        .send_keys("d")\
        .pause(0.2)\
        .send_keys(Keys.TAB * 3)\
        .pause(0.2)\
        .send_keys(Keys.ARROW_RIGHT * 2)\
        .pause(0.2)\
        .send_keys(Keys.TAB)\
        .pause(0.2)\
        .send_keys(Keys.ENTER)\
        .perform()
        
    print("Loading Image")
    
    image = driver.find_element(By.CSS_SELECTOR, "a[id^=imageDownload] img")
    ActionChains(driver)\
        .click(image)\
        .perform()
    print("Downloading Image")
    time.sleep(5)
    print("Image Downloaded. Quitting driver")
    driver.quit()
    print("driver closed.")


def main():
    DOWNLOAD_DIR = r"C:\Users\skyli\Downloads"
    WALLPAPER_DIR = r"C:\Users\skyli\Pictures"
    RESOLUTION = (3440, 1440)
    SLIDER_URL = r"https://rammb-slider.cira.colostate.edu/?sat=himawari&sec=full_disk&x=10868&y=16056&z=3&angle=0&im=18&ts=1&st=0&et=0&speed=170&motion=rock&refresh=1&maps%5Bborders%5D=slate&lat=0&p%5B0%5D=natural_color&p%5B1%5D=band_13&opacity%5B0%5D=1&opacity%5B1%5D=0.5&pause=20230221074000&slider=-1&hide_controls=0&mouse_draw=0&follow_feature=0&follow_hide=0&s=rammb-slider&draw_color=FFD700&draw_width=6"
    
    # Make sure directories are normalised in case anyone uses ~ or something
    WALLPAPER_DIR = os.path.abspath(WALLPAPER_DIR)
    DOWNLOAD_DIR = os.path.abspath(DOWNLOAD_DIR)
    
    # On startup, quickly sets the desktop to last image instead of black screen
    last_wallpaper = get_latest_image(WALLPAPER_DIR)
    if last_wallpaper:
        set_desktop_background(last_wallpaper)
    
    # Download new image. Takes 25-60s
    download_satellite_image(RESOLUTION, SLIDER_URL)
    
    # Move image to permanent place and set it as wallpaper
    download_path = get_latest_image(DOWNLOAD_DIR)
    new_path = move_image(download_path, WALLPAPER_DIR)
    set_desktop_background(new_path)


if __name__ == '__main__':
    main()



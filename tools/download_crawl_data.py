from distutils import dist
from google_drive_downloader import GoogleDriveDownloader as gdd
from my_kaggle_scripts.dataset.dataset_links import *
import os
from pathlib import Path


### !!  not used anymore, newer version
def download_raw_data(bot,opts,history):
    ##? https://github.com/ndrplz/google-drive-downloader
    ##? !pip install googledrivedownloader &> /dev/null
    

    os.makedirs('/kaggle/temp', exist_ok = True)
    if opts['mode'] == 'real_data':

        google_drive_file_ids = ['1sYziU0sCaSDh7GZSjTSa_4GHUSzVkpZ9','17tE3W7JHRu7sh-xYK34MOF4j6rhClxM2']
        for file_id in google_drive_file_ids:
            dest_path = '/kaggle/temp/real_videos_orginal.zip'
            gdd.download_file_from_google_drive(file_id=file_id,
                                                dest_path=dest_path,
                                                unzip=True, showsize=False, overwrite=True)
            file_size = os.path.getsize(dest_path)
            if file_size > 1000000000:break
    elif opts['mode'] == 'syntetic_data':

        if opts['synetic_data_ver'] == 0.01:
            google_drive_file_ids = ['1vmbb_lOxo_7zrmUR0RPEg1HOhEbNlfQN','14vLRf06ThbRr8kwjZjCktngOe3F15rR4']
            dest_path = '/kaggle/temp/SBVPI.zip'
        if opts['synetic_data_ver'] == 0.02:
            google_drive_file_ids = ['1PKnAn5dYDeFDTIUiqTpss0Y2QkGZAywL','19SXli2BLtr3-hGiQkRoO70N8qM-9tgbS']
            dest_path = '/kaggle/temp/syntetic_raw_images_ver_0.02.zip'
        for file_id in google_drive_file_ids:
            
            gdd.download_file_from_google_drive(file_id=file_id,
                                                dest_path=dest_path,
                                                unzip=True, showsize=False, overwrite=True)
            file_size = os.path.getsize(dest_path)
            if file_size > 10000000:break
        
    bot.send_message(text=f"💾 list dir  /kaggle/temp/: \n  {os.listdir('/kaggle/temp/')}") 
    bot.send_message(text=f"📤 list dir  /kaggle/working/ : \n {os.listdir('/kaggle/working/')}")
    bot.send_message(text=f'💾 {dest_path} : \n  {(file_size/1000000):.2f}  MB')

    history['ls after unzip for  /kaggle/temp/'] = os.listdir('/kaggle/temp/')
    history['ls after unzip for  /kaggle/working/'] = os.listdir('/kaggle/working/')
    history[f'{dest_path}'] = file_size/1000000
    return history



def download_raw_data_v2(links,opts,dist_dir = "../raw_videos/", quick_test = False):
    """
    mode : 'real_data','syntetic_data'
    syntetic_area : 'sclera','vessels','mix',

    """

    print('*'*25) 
    print(f"downloading {links['name']}") 

    mode =opts["mode"]
    

    Path(dist_dir).mkdir(parents=True, exist_ok=True)
    ## label:
    if links['label']:
        label_path = dist_dir + "label.csv"
        os.system(f"""wget -O {label_path} --no-check-certificate -q '{links['label']}&download=1'""")
        print('label downloaded')
    
    
    if mode == 'real_data':
        for file_name in links['links']:
            save_path = f"./{file_name}.zip"
            file_link = f"{links['links'][file_name]}&download=1"

            ##? download onedrive file : add &download=1 to end of anyone link
            print('-' * 25)
            os.system(f"""wget -O {save_path} --no-check-certificate -q '{file_link}'""")
            print('downloaded')
            os.system(f"""unzip -qq {save_path} -d {dist_dir}""")
            print('unziped')
            os.system(f"""rm {save_path}""")
            print('removed')
            print(file_name,'done')
            print(f"💾 {file_name} downloaded and unziped")
            if quick_test:break
    
    elif mode == 'syntetic_data':
        syntetic_area=opts['syntetic_area']
        save_path = f"./{syntetic_area}_mode.zip"
        file_link = f"{links[syntetic_area]}&download=1"

        ##? download onedrive file : add &download=1 to end of anyone link
        print('-' * 25)
        os.system(f"""wget -O {save_path} --no-check-certificate -q '{file_link}'""")
        print('downloaded')
        os.system(f"""unzip -qq {save_path} -d {dist_dir}""")
        print('unziped')
        os.system(f"""rm {save_path}""")
        print('removed')
        print(f"💾 {links[syntetic_area]} downloaded and unziped")


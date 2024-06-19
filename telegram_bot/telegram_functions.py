
##? https://api.telegram.org/bot1997635645:AAGx_NugrgHZbGaoueLsR0yR3itpFhWznKw/getUpdates  for geting chat_ID
##? !pip install python-telegram-bot &> /dev/null
##? https://www.emojiall.com/en/sub-categories/J1  emoji


"""

TODO: send colored text to telegram 


"""

import os,pickle
import telegram
import matplotlib.pyplot as plt
import time
from datetime import datetime
import pytz
import requests

# print('test auto reload 2')

def start_telegram_bot(bot_token,chat_id,history,PRINT=True,TELEGRAM=True):
    
    now = datetime.now(pytz.timezone('Asia/Tehran'))
    date_string = now.strftime("%d/%m/%Y %H:%M:%S")
    bot = log_agent(bot_token=bot_token,chat_id=chat_id, PRINT=PRINT, TELEGRAM=TELEGRAM)
    bot.send_message(text="🚩"*15)
    bot.send_message(text="👇"*15)
    bot.send_message(text=f"bot_token ={bot_token}")
    bot.send_message(text=f"start date_time ={date_string}")    
    history['start_time'] = date_string
    history['bot_token'] = bot_token
    return bot,history

def send_opts_to_telegram(bot,opts):
    bot.send_message(text='#real_video_training #transfer learning')
    bot.send_message(text='🔧'*10)
    for key in opts:
        bot.send_message(text=f'🔧 {key} :  {opts[key]}')
        time.sleep(0.3)
    bot.send_message(text='🔧'*10)

class log_agent():
    def __init__(self, bot_token, chat_id, PRINT,TELEGRAM):
        bot_token_1 = 'your_bots API' #kaggle_model_1
        bot_token_2 = 'your_bots API' #kaggle_model_2
        bot_token_3 = 'your_bots API' #kaggle_model_3
        self.tokens = [bot_token_1,bot_token_2,bot_token_3]
        self.bot_token = bot_token
        self.bot = telegram.Bot(token=bot_token)
#         self.bot_data = telegram.Bot(token=bot_token_5)
        self.chat_id = chat_id
        self.temp = {}
        os.makedirs('./model_save/', exist_ok = True)
        
        print('telegram_agent initiated')
        
    def send_message(self,text,reply_to_message_id=None,PRINT=True,TELEGRAM=True):

        res = None
        if TELEGRAM:
            try:
                res = self.bot.send_message(text=text, chat_id=self.chat_id,reply_to_message_id = reply_to_message_id,timeout=50)
            except Exception as e:
                print("!!! telegram bot error")
                print(e)
        if PRINT:
            print(text)
        return res
    
    def send_photo(self, photo_binery=None, photo_address=None):
        
        try:
            if photo_binery: 
                res = self.bot.send_photo(chat_id=self.chat_id, photo=photo_binery, caption=None)
                return res
            elif photo_address:
                photo = open(photo_address,'rb')
                res = self.bot.send_photo(chat_id=self.chat_id, photo=photo, caption=None)
                return res
            else:
                print('! you must input image file or address.')
        except Exception as e:
            print("!!! telegram bot error")
            print(e)
    
    def edit_message_text(self,text ,message_id=None):
        res = self.bot.edit_message_text(text, chat_id = self.chat_id, message_id=None)
        return res

    def forward_message(self,from_chat_id=None, message_id=None):
        res = self.bot.forward_message(chat_id=self.chat_id, from_chat_id=from_chat_id, message_id=message_id)
        return res

    def send_document(self, document=None, filename=None, caption=None, mode='main_bot'):
        res = None
        try:
            res = self.bot.send_document(chat_id=self.chat_id, document=document, filename=filename, caption=caption,timeout=150)
            return res
        except Exception as e:
            print("!!! telegram bot error")
            print(e)
        
        return res


    def get_file_link(self, file_id=None,file_bot_token=None ):

        try:
            if file_bot_token:
                try:
                    temp_bot = telegram.Bot(token=file_bot_token)
                    res = temp_bot.get_file(file_id=file_id,timeout=100)
                    return res,file_bot_token
                except Exception as e:
                    print(e)
            else:    
                for file_bot_token in self.tokens:
                    try:
                        temp_bot = telegram.Bot(token=file_bot_token)
                        res = temp_bot.get_file(file_id=file_id,timeout=100)
                        return res,file_bot_token
                    except:
                        print('@')
        except Exception as e:
            print("!!! telegram bot error")
            print(e)    
            return None,None
    
    def send_file(self,file_address=None,CHUNK_SIZE=19000000,file_name='myfile',file_format ='.tar'):
        
        try:
            self.send_message(text= f"start uploading ...")
            self.temp = {'model_files':[]}
            os.makedirs('./splited_files_for_send/', exist_ok = True)
            file_number = 1
            with open(file_address,'rb') as f:
                chunk = f.read(CHUNK_SIZE)
                while chunk:
                    with open(f'./splited_files_for_send/{file_name}_{file_number}.{file_format}','wb') as chunk_file:
                        chunk_file.write(chunk)
                    with open(f'./splited_files_for_send/{file_name}_{file_number}.{file_format}','rb') as chunk_file:
                        res = self.send_document(document=chunk_file)  
                        self.send_message(text = str(res['document']['file_id']),reply_to_message_id=res['message_id'],PRINT=False)
                        self.temp['model_files'].append((res['document']['file_name'],res['document']['file_id']))
                    file_number += 1
                    chunk = f.read(CHUNK_SIZE)
            return self.temp
        except Exception as e:
            print("!!! telegram bot error")
            print(e)
            return None

    def make_image(self,history=None,caption='',
                    send_telegram=True,show=True,
                    model_type = "classification"):
        try:
            fig1 = plt.figure(figsize=(10,5))
            plt.title("Training and Validation Loss", figure=fig1)
            plt.plot(history['val_history']['loss'],label="validation_loss", figure=fig1)
            plt.plot(history['train_history']['loss'],label="train_loss", figure=fig1)
            plt.xlabel("iterations", figure=fig1)
            plt.ylabel("Loss", figure=fig1)
            plt.legend()
            fig1.savefig('./Graph1.png')
            self.send_photo(photo_address='./Graph1.png')
            
            if model_type == "classification":
                plot_data_val = history['val_history']['acc']
                plot_data_train = history['train_history']['acc']
                plot_text = "Training and Validation ACC."
                ylabel_text = "acc %"
            elif model_type == "regression":
                plot_data_val = history['val_history']['R2_score']
                plot_data_train = history['train_history']['R2_score']
                plot_text = "Training and Validation R2_score."
                ylabel_text = "R2_score value"



            fig2 = plt.figure(figsize=(10,5))
            plt.title(plot_text, figure=fig2)
            plt.plot(plot_data_val,label="val", figure=fig2)
            plt.plot(plot_data_train,label="train", figure=fig2)
            plt.xlabel("iterations", figure=fig2)
            plt.ylabel(ylabel_text, figure=fig2)
            plt.legend()
            fig2.savefig('Graph2.png')
            self.send_photo(photo_address='./Graph2.png')
            
            fig3 = plt.figure(figsize=(10,5))
            plt.title("Learning Rates", figure=fig3)
            plt.plot(history['learning_rates'],label="value of LR", figure=fig3)
            plt.xlabel("iterations", figure=fig3)
            plt.ylabel("LR", figure=fig3)
            plt.legend()
            fig3.savefig('Graph3.png')
            self.send_photo(photo_address='./Graph3.png')
            plt.show()
        except Exception as e:
            print("!!! telegram bot error")
            print(e)
    
    def merge_cb(self,f, s):
        print("file: {0}, size: {1}".format(f, s))
    
    def download_log(self,log_file_id):
        try:
            os.makedirs('./load_stuff/', exist_ok = True)
            log = self.get_file_link(file_id=log_file_id)
            log.download(custom_path='./load_stuff/logs_downloaded.pickle', out=None, timeout=150)
            return log
        except Exception as e:
            print("!!! telegram bot error")
            print(e)
            return None
    
    def download_model(self,log_file_id):
        
        os.makedirs('./load_stuff/', exist_ok = True)
        os.makedirs('./loaded_model_parts/', exist_ok = True)
        os.makedirs('./loaded_model/', exist_ok = True)
        files = []
        log,file_bot_token = self.get_file_link(file_id=log_file_id)
        log.download(custom_path='./load_stuff/logs_downloaded.pickle', out=None, timeout=200)
        with open('./load_stuff/logs_downloaded.pickle', 'rb') as handle:
            log = pickle.load(handle)
            
        last_epoch = list(log['model_files'].keys())[-1]

        for file_id in log['model_files'][last_epoch]['model_files']:
            print(file_id)
            temp_var,file_bot_token = self.get_file_link(file_id=file_id[1],file_bot_token=file_bot_token)
            custom_path = './loaded_model_parts/'+ file_id[0]
            temp_var.download(custom_path= custom_path, out=None, timeout=150)
            files.append(custom_path)
            time.sleep(1)
            
        out_data = b''
        for fn in files:
            with open(fn, 'rb') as fp:
                out_data += fp.read()
        with open(f"./loaded_model/{log['opts']['model_type']}.tar", 'wb') as fp:
            fp.write(out_data)
        print('model loaded and merged')
        return log


    def get_new_order_from_telegram_bot(self,train_start_epoch_time,try_limit = 3):
        """
        todo orders: 
        1 - change train parameters like LR
        2 - save and upload model
        3 - change some of opts
        """
        try_count = 0
        new_order = None
        while True:
            try:
                r = requests.get(f'https://api.telegram.org/bot{self.bot_token}/getUpdates')
                assert r.status_code == 200
                response = r.json()
                if len(response['result']) > 0:
                    last_chat_total = response['result'][-1]
                    last_chat_update_id = int(last_chat_total['update_id'])
                    last_chat_text = str(last_chat_total['message']['text'])
                    last_chat_date = int(last_chat_total['message']['date'])
                    
    #                 print(last_chat_text)
                    if last_chat_date > train_start_epoch_time:
                        new_order = last_chat_text
                break
            except Exception as e:
                try_count += 1 
                if try_count > try_limit:
                    print("!!!!!!!!!!")
                    print(e)
                    return None
                    
        if new_order == "cancel":
            self.send_message(text=f"get order for cancel train | raise value error.")
            raise Exception("new_order_from_telegram_bot")
            
        

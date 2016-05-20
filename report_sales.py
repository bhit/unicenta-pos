from pymysql import connect, err, sys, cursors # sql
import datetime                 # date
import os                       # file operations
from ftplib import FTP          # upload to server
import smtplib                  # sending email

'''
Preliminary variables
'''
storename = 'redacted'
today = datetime.datetime.today()
root_path = "redacted"
os.chdir(root_path)


# Create a new folder for today if we can
new_path = root_path+"\\"+ today.strftime('%Y%m%d')
if not os.path.exists(new_path):
    os.makedirs(new_path)

def retrieve_cash(date):

    '''
    Retrieves the list of cash payments made during the selected date.
    The date must be written in the datetime format. 
    '''

    date_to_search = date
    
    # Connect to mysql
    conn = connect(host = 'localhost', port = 3306,
                   user = 'redacted', passwd='redacted', db='unicentaopos')
    cursor = conn.cursor(cursors.DictCursor)
    
    # Fetch data from the RECEIPTS table
    # then collect the IDs of all of today's transactions
    id_list = []
    cursor.execute("SELECT * FROM `receipts`")
    data = cursor.fetchall()
    for dt in range(len(data)):
        if data[dt]['DATENEW'].date() == date_to_search:
            id_list.append(data[dt]['ID'])

    # Find cash exchanged from the MONEY column in table PAYMENTS
    cash_list = []
    for idl in id_list:
        cursor.execute("SELECT * FROM `payments` WHERE `RECEIPT` like " 
                       + "'%" + idl + "%'" )
        data = cursor.fetchall()
        cash_list.append(data[0]['TOTAL'])

    print "Processed " + str(len(id_list)) + " payments "

    return id_list, cash_list

def create_file_content(cash_list):
    content_list = []
    for csh in cash_list:
        content_list.append(str(storename) + str(today.strftime('%Y%m%d')) + str(csh))
    return content_list

def write_file(content_list):
    count = 1
    file_list = []
    os.chdir(new_path)    
    for fle in content_list:
        filename = storename + "." +  "{0:0>3}".format(count)

        with open(filename, "w") as text_file:
            text_file.write(fle)
            
        file_list.append(filename)        
        count += 1
        print "Writing file " +  filename

    return file_list


def write_to_server(date, file_list):
    '''
    Server details
    '''

    # Set up the server details
    folder_name = date.strftime('%Y%m%d')
    server_address = 'redacted'
    ftp = FTP(server_address, 'redacted', 'redacted')

    # Switch to the file directory and create a folder with today's date
    ftp.cwd("public_html")
    try:
        ftp.mkd(folder_name)
        print "Created today's folder"
    except:
        pass
    
    # Switch to the files for today
    ftp.cwd(folder_name)    
    os.chdir(new_path)
    
    # Start uploading files
    for fle in file_list:
        try:
            file_path = new_path + "\\" + str(fle)
            print "Uploading " + str(file_path)
            print "\t ... to " + fle
            ftp.storbinary('STOR ' + fle, open(file_path, 'rb'))

        except:
            pass

    print "Finished uploading files to server"
        
    ftp.quit()

'''
Send an email with today's sales figures
'''    
def mail_update(cash_list):
    # Assemble the message to be sent out
    msg = ""
    for trans in cash_list:
        msg = msg + str(trans) + "\n"
    msg = msg + "----------" + "\n"
    print "Total sales today were " + str(sum(cash_vec) )
    msg = msg + "Total " + str(sum(cash_list))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("redacted", "redacted")
    server.sendmail("redacted", "redacted", msg)

    print "Sent sales update to store email"
    
    server.quit()
    

# Today's date
today = datetime.datetime.today().date()

# Generate the cash list, file contents
id_vec, cash_vec = retrieve_cash(today)
content_vec = create_file_content(cash_vec)
file_vec = write_file(content_vec)
write_to_server(today, file_vec)
mail_update(cash_vec)

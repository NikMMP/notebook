import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from django.conf import settings


# to get refresh_token
# curl https: // api.dropbox.com/oauth2/token \
#     - d code = AUTHORIZATIONCODEHERE \
#     - d grant_type = authorization_code \
#     - u APPKEYHERE: APPSECRETHERE​

DROPBOX_REFRESH_TOKEN = "ujDoMrsSRtEAAAAAAAAAAZyxbAPHLi2iDmjR69I33g6_ADQFeR7NTCjVUlDcNsJV"
DROPBOX_APP_KEY = "tl0qxl76p062gp9"
DROPBOX_APP_SECRET = "fo08nr74ftqcojl"

refresh_token = DROPBOX_REFRESH_TOKEN
app_key = DROPBOX_APP_KEY
app_secret = DROPBOX_APP_SECRET

# refresh_token = settings.DROPBOX_REFRESH_TOKEN
# app_key = settings.DROPBOX_APP_KEY
# app_secret = settings.DROPBOX_APP_SECRET

UPLOADFILE = "dropbox_download.txt"
BACKUPPATH = "/docs/dropbox_download.txt"
DOWNLOADFILE = "dropbox_download.txt"


class DropBoxServer:
    def __init__(self, refresh_token, app_key, app_secret):
        self.dbx = dropbox.Dropbox(
            app_key=app_key,
            app_secret=app_secret,
            oauth2_refresh_token=refresh_token
        )

    def connect(self):
        try:
            self.dbx.users_get_current_account()
        except AuthError:
            sys.exit("ERROR: Invalid access token; try re-generating an "
                     "access token from the app console on the web.")

    def filelist(self, dropbox_filepath):
        return self.dbx.files_list_folder(dropbox_filepath).entries

    def download(self, dowload_file, backup_file):
        print("Downloading current " + backup_file +
              " from Dropbox, overwriting " + dowload_file + "...")
        self.dbx.files_download_to_file(dowload_file, backup_file)

    def backup(self, upload_file, backup_file):
        with open(upload_file, 'rb') as f:
            # We use WriteMode=overwrite to make sure that the settings in the file
            # are changed on upload
            print("Uploading " + upload_file +
                  " to Dropbox as " + backup_file + "...")
            try:
                self.dbx.files_upload(f.read(), backup_file,
                                      mode=WriteMode('overwrite'))
            except ApiError as err:
                # This checks for the specific error where a user doesn't have
                # enough Dropbox space quota to upload this file
                if (err.error.is_path() and
                        err.error.get_path().reason.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                    sys.exit()
                else:
                    print(err)
                    sys.exit()

    def delete(self, file_to_delete):
        self.dbx.files_delete_v2(file_to_delete)


# dbx = DropBoxServer(refresh_token=refresh_token,
#                     app_key=app_key, app_secret=app_secret)
# dbx.connect()

# print("list of files and folders")
# list = dbx.filelist("")
# for file in list:
#     print(file.name)

# print(f"upload file: {UPLOADFILE}")
# # backup(dbx, UPLOADFILE, BACKUPPATH)
# dbx.backup(UPLOADFILE, BACKUPPATH)
# print("uploading complete")

# print(f"download file: {BACKUPPATH} from Dropbox")
# dbx.download(DOWNLOADFILE, BACKUPPATH)
# print("downloading complete")

# print(f"deleting file {BACKUPPATH}")
# dbx.delete(BACKUPPATH)
# print("deletion complete")

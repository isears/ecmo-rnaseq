#!/users/isears1/anaconda/rnaseq/bin/python

import ftplib
import glob
import time

# God save us
# https://stackoverflow.com/questions/33438456/python-ftps-upload-error-425-unable-to-build-data-connection-operation-not-per
class Explicit_FTP_TLS(ftplib.FTP_TLS):
    """Explicit FTPS, with shared TLS session"""

    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(
                conn, server_hostname=self.host, session=self.sock.session
            )
        return conn, size


def ftp_connect():
    ftp = Explicit_FTP_TLS("usegalaxy.org")
    passwd = open("./ugp.txt", "r").readlines()[0].strip()
    ftp.set_debuglevel(2)
    ftp.login("isaac_sears@brown.edu", passwd)
    ftp.prot_p()
    ftp.voidcmd("TYPE I")
    ftp.set_pasv(True)

    return ftp


if __name__ == "__main__":
    ftp = ftp_connect()

    for fname in glob.glob(
        "/gpfs/home/isears1/Repos/ecmo-rnaseq/data/30-573159527/00_fastq/*.fastq.gz"
    ):

        finished = False
        upname = fname.split("/")[-1]
        print(f"[*] Attempting to upload: {fname} as {upname}")

        with open(fname, "rb") as f:
            while not finished:
                try:
                    if ftp is None:
                        print("Connecting...")
                        ftp = ftp_connect()

                    if f.tell() > 0:
                        rest = ftp.size(upname)
                        print(f"Resuming transfer from {rest}...")
                        f.seek(rest)
                    else:
                        print("Starting from the beginning...")
                        rest = None
                    ftp.storbinary(f"STOR {upname}", f, rest=rest)
                    print("Done")
                    finished = True
                except Exception as e:
                    ftp = None
                    sec = 5
                    print(f"Transfer failed: {e}, will retry in {sec} seconds...")
                    time.sleep(sec)

        # Debug
        # with open("test.txt", "rb") as f_up:
        #     ftp.storbinary("STOR test2.txt", f_up)

        print("\n")

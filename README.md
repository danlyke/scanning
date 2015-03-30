# Simple Scan Manager

We recently got a Brother All-In-One that has a sheet fed
scanner. This scanner can send its scans to an FTP server.

We're thinking about paperless, and realized that it doesn't do
anything to scan files if you can't do anything with them.

So: This is a total hack, uses PostgreSQL and Perl on my home
server. If you decided to base anything off of it please email me and
we'll figure out how to at least make it installable.

## General Architecture

The FTP uploads on the local network (yay unencrypted FTP) to a
"brscanner" account in /home/brscanner, with UID 1003.

My work directory is /home/danlyke/scanning, and the web portion of
the project lives at /var/www/scanning protected by an htpasswd file,.

   gcc -o importsetuid importsetuid.c
   sudo chown root importsetuid
   sudo chmod +s importsetuid

This runs import.pl as user/group 1003/1003 (brscanner).

**import.pl** scans the imported PDFs, creates 640 pixel wide thumbnails,
and copies the PDFs to two different drives.

/var/www/scanning/files should be owned by 1003.

## CGIs

These should go in /var/www/scanning

**index.cgi** lets you browse.

**edit.cgi** lets you edit. Note that the DBI stuff should be rewritten to
use bound variables because of the "DBI::quote takes an array" issue,
the directory is password protected and if there's someone nefarious
there I'm hosed anyway.





.. code-block:: cpp
   :linenos:

   /* This is bad. Reaaly bad. It's a really, really bad hack. If you're an employee of
    * Intertrode Communication, then I'm really, really sorry that you have to maintain
    * this. I was honestly planning on removing this tomorrow, but I've been known to
    * forget things like this. It happens.
    *
    * So here's the thing. I can't seem to figure out why the AccountId variable isn't
    * set. I've looked and looked, but I gotta leave now. Anyway, I've found that I can
    * just grab the AccountID from the debugging logs.  I suppose that to fix it, you'd
    * have to locate where it's clearing out the ID.
    *
    * Again, I'm sorry.
    */

   if ( (AccountId == NULL) || (AccountId == "") ||
        (ServerSesion["AccountId"] == NULL) || (ServerSesion["AccountId"] == "") )
   {
      //open session logs
      FileHandle file = f_open(LOG_PATH + "\sessionlog-" + LOG_FILE_DATE + ".log", 1);
      while (file != NULL)
      {

         TString line = f_readline(file);

         //look for IP and changereg
         if ( (sfind(line,REMOTE_ADDR) != -1) && (sfind(line,"changereg") != -1) )
         {
            //0000-00-00 00:00 /accountmaint/changereg/?AccountId=123456 255.255.255.255 ...
            //                                                    *
            AccountId = substr(line, 52, 6);
         }

         if (f_EOF(file)) { f_close(file); file = NULL; }
      }

   }

As GitHub gist: https://gist.github.com/ivangeorgiev/96d7321b3edc5f4ac8ae808e75cca16a

Origin: https://www.badprogramming.com/code/Retrieving-an-accountId-in-the-log


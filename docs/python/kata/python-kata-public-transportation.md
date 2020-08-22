# Public Transportation - Python Kata

Imagine you live in Amsterdam and you want to travel to Paris. Of course you want to travel as soon as possible, but you have to take in account the railways timetable. Railways work in batch mode. They come on a schedule, pick everybody from the train station and move them. 

In our software development practice we face similar problems every day. Here is a similar one.

## Problem

Files are being delivered by multiple source systems into a staging folder. These files are our passengers. You need to create a solution which periodically is taking a list of available files and is processing them by extracting the words from the files and inserting into a database table. This is processing solution is our train. In fact what we are creating is a pipeline. The pipeline is using batches - the list of available files.

Think about following:

* How do you test your solution?
* How do you handle exceptions?
* How easy is for other people (or you after a year) to read and understand your solution? 
* How would you add pre- and post-processing of words to your pipeline? For example, as pre-processing you might need to convert the word to lower case, strip punctuation characters. Post-processing might be to sleep for 2 seconds.
* How would you add pre- and post-processing of batches to your pipeline? For example, as post-processing, you might want to sleep for 20 seconds.
* How would you reuse this solution in other scenarios? For example - your staging is a database table and as processing an email is sent.


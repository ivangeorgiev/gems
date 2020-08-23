# Iterate over hierarchical sources in Python

## Problem

### Scenario

We are given a list of files and we need to insert the words from files into a database. The sequence of the words should be preserved. 

Here is one way to achieve this:

```python
file_list = ['a.txt', 'b.txt']
for file_name in file_list:
    with open(file_name, 'r') as file:
        for line in file.readline():
            for word in line.split(' '):
                with db.connection.cursor() as cursor:
                    cursor.execute('INSERT INTO words(word) VALUES (?)', (word,))
                    cursor.commit()
```

Wow. Not very easy to read already, but it serves the purpose.

How about testing? You think - it is pretty straightforward. *"I did couple of exploration tests during development. I am pretty confident it works!"* Well ... wait to see what comes next. 

**Day 1.** New requirements:

1. Stop words should be inserted into a table `stop_words`. Rest of the words are still going into the `words` table.

**Day 2.** New requirements:

1. Our database administrator has some concerns about the performance and wants that the commit statement happens after 1000 words has been inserted into each table. This means you keep track on number of inserted words in each table separately. When any of the table reaches 1000 you commit inserts for that table and reset the counter for that table.

**Day 3.** 

1. New requirement: We should be able to extract words from Word files.
2. Bug: words are not split on punctuation.
3. Bug: multiple spaces cause empty words to be inserted.
4. New requirement: words need to be stored in lower case.

**Week 5.** You worked very hard, but you are still unable to finish the Word files processing. Your manager asks you to deliver without this feature. She also assigns three new developers to your project as new requirements arrive.

1. You need to be able to process PDF files

**Week 25.** Everything works more or less fine. Now the privacy team comes into the picture.

1. Only approved files should be processed. You receive a list of approved files in a CSV file.
2. You need to be able to OCR images
3. You need to create a build pipeline for continuous integration
4. The solution needs to implement unit tests with at least 70% coverage. Unit tests should be executed at build time.

**Year 1.**

1.  Privacy team has provided REST API to validate the file eligibility for processing. Can you remember how the whole this hell thing works?
2. Real-time processing! List of files is stored in a database table. It is updated constantly. Our solution needs to process each new file entry as soon as possible.
3. We want that words are inserted not only into the database, but also sent to a message queue.

### What if?

What if our processing looks like this:

```python
for word in extract_words():
    process_word(word)
```

Even better:

```python
db_processor = word_process.get_database_processor()
extractor = word_extract.get()
reader.when_new_word(processor.process)
```

## Solution

Let's start with the original requirements. Can we make the code more readable
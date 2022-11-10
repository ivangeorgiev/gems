# Regular Expression (regex) to match UUID string

Following regular expression matches a hyphen-delimited UUID hex string:

```
^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$
```

Because hyphens are present in fixed places, to preserve bandwidth and storage, they are often omitted. Following regex makes hyphens optional:

```
^[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{4}-?[0-9a-fA-F]{12}$
```



Some UUIDs to test the regex matches with:

```
1bd36deb-bdf3-4692-8079-0ba9c648aabc
ad40e41e-4f3c-42E4-AA01-5751b9404907
ad40e41e4f3c42e4aa015751b9404907
```





See also:

* https://ihateregex.io/expr/uuid/
* https://regex101.com/
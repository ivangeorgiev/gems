# Replace substring in a string

## Pattern expansion

To replace the first occurance of a substring into a string:

```bash
${input_variable_name/search_string/replacement}
```

To replace all occurances of a substring into a string:

```bash
${input_variable_name//search_string/replacement}
```

## Examples

Following example substitues the first occurance of the pattern. In this case the character `a` is being replaced by dash `-`:

```bash
$ the_input=baobab
$ echo ${the_input/a/-}
b-obab
```

Similarly we could replace all occurencies of the pattern:

```bash
$ the_input=baobab
$ echo ${the_input//a/-}
b-ob-b
```

Here we illustrated only simple string replacement. It is possible to use patterns. For details, refer to [Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html).

## See also

* Gnu's [Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)

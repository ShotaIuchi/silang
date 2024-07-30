# silang

si language

## syntax (plan)

###　 value

```si
val const_explicitly: int = 0
val const_implicit = 0
val const_implicit_float = 0f

var non_const_explicitly: int = 0
var non_const_implicit = 0
var non_const_implicit_float = 0f

// const_explicitly = 1             // NG
// const_implicit = 1               // NG
// const_implicit_float = 1f        // NG

non_const_explicitly = 1            // OK
non_const_implicit = 1              // OK
non_const_implicit_float = 1f       // OK
```

### function

```si
bool function(src: int, dst: &int):
    dst = src
```

### if

```si
if (a == 0):
    print('if')
ei (b == 0):
    print('else if')
no:
    print('else')
```

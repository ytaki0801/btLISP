# blSECD: A SECD-style virtual machine

## outline of specification

### Stacks

* S: stack to work
* E: env to keep closure values
* C: stack of VM codes
* D: stack to dump to recur or branch

### Instructions

* LD: pop a closure value specified by a C code from E and push it to S
* LF: pop a closure from C and push it with the current E to S
* LV: load a constant value or a built-in function and push it to S
* AP: pop a function with a value from S, if the function is a built-in function: apply and push the result to S, if the function is a closure: dump (S E C) to D, clear S, set the closure body to C and set the pair of the value and the closure variable to E
* RT: pop (S E C) from D, set the current top of the value in S following by poped S to S, set the poped E to E and set the poped C to C
* SL: pop true and false codes from C, dump the current C to D,
    pop a conditional value from C and set the true or false code to C
* JI: pop C from D and push it to C
* ST: stop vm


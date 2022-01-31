# v1: extention of v0 specification

* compiler: `nil`, int without `quote`, `lambda` multi arguments, `list`, `urec`
	* `bl-comp1.bl0`: v1 compiler running on v0 interpreter or by compiler with vm
	* `bl-comp1.bl1`: v1 compiler running by v1 compiler with vm only

* built-in functions: `intp`, `add`, `sub`, `mul`, `div`, `quo`, `rem`, `lt`, `gt`

* S-expression input function: comment

Note: Conscell with dot notation and alist and global variables may not supported also in future.


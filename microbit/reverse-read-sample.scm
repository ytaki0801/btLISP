(write
  (((lambda (u) (u u)) (lambda (u)
    (lambda (x y)
      (if (eq? x (quote ())) y
          ((u u) (cdr x) (cons (car x) y))))))
   (read (current-input-port)) (quote ())))

;;;;
;;;; bl-comp.scm:
;;;; btLISP Scheme-subset compiler in Scheme-subset for blSECD
;;;;
;;;; (C) 2022 TAKIZAWA Yozo
;;;; This code is licensed under CC0.
;;;; https://creativecommons.org/publicdomain/zero/1.0/
;;;;

;;;; compile btLISP Scheme-subset codes to blSECD virtual machine codes
;;;; s: LISP codes from C, e: positions of closure vals in E, c: next codes
(write (((lambda (U) (U U)) (lambda (U) (lambda (s e c)

   ;;;; pair list
   (if (pair? s)

       ;;;; quote
       (if (eq? (car s) (quote quote))
           (cons (quote ldc) (cons (car (cdr s)) c))

       ;;;; if
       (if (eq? (car s) (quote if))
           ((lambda (t f)
              ((U U) (car (cdr s)) e
                     (cons (quote btf) (cons t (cons f c)))))
             ((U U) (car (cdr (cdr s)))       e (quote (jtf)))
             ((U U) (car (cdr (cdr (cdr s)))) e (quote (jtf))))

       ;;;; lambda
       (if (eq? (car s) (quote lambda))
           ((lambda (v b)
              ((lambda (br)
                 (cons (quote ldf)
                    (cons ((U U) br (cons (car v) e) (quote (rtn))) c)))
               (if (eq? (cdr v) (quote ())) b
                   ;;;; recursive expansion for multi argumens of lambda
                   (cons (quote lambda) (cons (cdr v) (cons b (quote ())))))))
            (car (cdr s)) (car (cdr (cdr s))))

       ;;;; current-input-port as a dummy
       (if (eq? (car s) (quote current-input-port))
           (cons (quote ldc) (cons (quote ()) c))

       ;;;; generate codes to apply a function
       ((lambda (f a r apd)
          (((lambda (W) (W W)) (lambda (W) (lambda (t r)
             (if (eq? r (quote ())) (apd t c)
                 ;;;; recursive apply for multi argumens of lambda
                 ((W W) ((U U) (car r) e (apd t (quote (app))))
                        (cdr r))))))
           ((U U) a e ((U U) f e (quote (app)))) r))
        (car s) (car (cdr s)) (cdr (cdr s))
        ((lambda (V) (V V)) (lambda (V) (lambda (a b)
           (if (eq? a (quote ())) b
               (cons (car a) ((V V) (cdr a) b)))))))))))

   ;;;; a constant value or a pos of a closure variables from E to set S
   ((lambda (p)
      (if (eq? p (quote ())) (cons (quote ldc) (cons s c))
                             (cons (quote ldv) (cons p c))))
    (((lambda (W) (W W)) (lambda (W) (lambda (s e n)
        (if (eq? e (quote ())) (quote ())
        (if (eq? s (car e)) n ((W W) s (cdr e) (+ n 1)))))))
     s e 0))))))

 ;;;; read S-expression, initialize env as () and (stp) as final code
 (read (current-input-port)) (quote ()) (quote (stp))))


#lang plait

(define-type-alias Value Number)

(define-type Op ;⊕
  (add)
  (sub)
  (mul)
  (lq))

(define-type Exp ;e
  (numE [n : Value])
  (varE [x : Symbol])
  (opE  [e1 : Exp] [op : Op] [e2 : Exp])
  (ifzE [con : Exp] [t : Exp] [f : Exp]) ;condition, true, false
  (letE [s : Symbol] [e1 : Exp] [e2 : Exp])
  (funE [name : Symbol] [args : (Listof Exp)]))

(define-type Def ;d
  (defE [name : Symbol] [args : (Listof Symbol)] [val : Exp]))

(define-type Pro ;p
  (proE [definitions : (Listof Def)] [body : Exp]))

; (parse-program `{define {[fun f (a b c) = {{a + b} <= c}] [fun g () = 8]} for 7})

; parse---------------------------------------------------------------
(define (parse-program [s : S-Exp]) : Pro
  (if (s-exp-match? `{define ANY for ANY} s)
      (proE (parse-definitions (s-exp->list (second (s-exp->list s))))
            (parse-expression  (fourth (s-exp->list s))))
      (error 'parse-program "incorrect program representation")))

(define (parse-definitions [defs-list : (Listof S-Exp)]) : (Listof Def)
  (if (empty? defs-list)
      (list)
      (cons (parse-def (first defs-list)) (parse-definitions (rest defs-list)))))

(define (parse-def [s : S-Exp]) : Def
  (if (s-exp-match? `{fun ANY ANY = ANY} s)
      (defE (s-exp->symbol (second (s-exp->list s)))
        (map s-exp->symbol (s-exp->list (third (s-exp->list s))))
        (parse-expression (list-ref (s-exp->list s) 4)))
      (error 'parse-def "incorrect definition representation")))

(define (parse-expression [s : S-Exp]) : Exp
  (cond
    [(s-exp-match? `NUMBER s) (numE (s-exp->number s))]
    [(s-exp-match? `SYMBOL s) (varE (s-exp->symbol s))]
    [(s-exp-match? `{ANY SYMBOL ANY} s)
     (opE
      (parse-expression (first (s-exp->list s)))
      (parse-op (second (s-exp->list s)))
      (parse-expression (third (s-exp->list s))))]
    [(s-exp-match? `{ifz ANY then ANY else ANY} s)
     (ifzE
      (parse-expression (list-ref (s-exp->list s) 1))
      (parse-expression (list-ref (s-exp->list s) 3))
      (parse-expression (list-ref (s-exp->list s) 5)))]
    [(s-exp-match? `{let SYMBOL be ANY in ANY} s)
     (letE
      (s-exp->symbol(list-ref (s-exp->list s) 1))
      (parse-expression (list-ref (s-exp->list s) 3))
      (parse-expression (list-ref (s-exp->list s) 5)))]
    [(s-exp-match? `{SYMBOL ANY} s)
     (funE
      (s-exp->symbol (list-ref (s-exp->list s) 0))
      (parse-listof-exp (s-exp->list (list-ref (s-exp->list s) 1))))]
    [else (error 'parse-expression "incorrect expression representation")]))
      
(define (parse-op [s : S-Exp]) : Op
  (cond
    [(s-exp-match? `+ s) (add)]
    [(s-exp-match? `- s) (sub)]
    [(s-exp-match? `* s) (mul)]
    [(s-exp-match? `<= s) (lq)]
    [else (error 'parse-op "unknown operator")]))

(define (parse-listof-exp [s : (Listof S-Exp)]) : (Listof Exp)
  (if (empty? s)
      (list)
      (cons (parse-expression (first s)) (parse-listof-exp (rest s)))))

; eval----------------------------------------------------------------

; variables enviromet
(define-type Binding
  (bind [name : Symbol]
        [val : Value]))

(define-type-alias Env (Listof Binding))

(define mt-env empty)

(define (extend-env [env : Env] [x : Symbol] [v : Value]) : Env
  (cons (bind x v) env))

(define (lookup-env [n : Symbol] [env : Env]) : Value
  (type-case (Listof Binding) env
    [empty (error 'lookup "unbound variable")]
    [(cons b rst-env) (cond
                        [(eq? n (bind-name b))
                         (bind-val b)]
                        [else (lookup-env n rst-env)])]))
; functions enviroment
(define-type Binding-f
  (bind-f [name : Symbol]
          [args : (Listof Symbol)]
          [val : Exp]))

(define-type-alias Env-f (Listof Binding-f))

(define mt-env-f empty)

(define (extend-env-f [env-f : Env-f] [df : Def]) : Env-f
  (cons (bind-f (defE-name df) (defE-args df) (defE-val df))
        env-f))

; zwraca exp - cialo funkcji oraz srodowisko w jakim sie ona liczy
(define (lookup-env-f [sym : Symbol] [args : (Listof Value)] [env-f : Env-f]) : (Exp * Env)
  (if (empty? env-f)
      (error 'lookup-env-f "undefined function")
      (if (equal? sym (bind-f-name (first env-f))) ;porownanie nazwy
          (if (= (length args) (length (bind-f-args (first env-f)))) ;sprawdzenie ilosci argumentow
              (pair (bind-f-val (first env-f))
                    (make-function-enviroment args (bind-f-args (first env-f))))
              (error 'lookup-env-f "wrong number of arguments"))
          (lookup-env-f sym args (rest env-f)))))

(define (make-function-enviroment [args : (Listof Value)] [names : (Listof Symbol)]) : Env
  (if (empty? args)
      (list)
      (cons (bind (first names) (first args)) (make-function-enviroment (rest args) (rest names)))))

(define (eval-op [o : Op]) : (Number Number -> Number)
  (type-case Op o
    [(add) +]
    [(sub) -]
    [(mul) *]
    [(lq) (lambda (x y) (if (<= x y)
                            0
                            42))]))

(define (eval-exp [e : Exp] [env : Env] [env-f : Env-f]) : Number
  (type-case Exp e
    [(numE x)
     x]
    [(varE x)
     (lookup-env x env)]
    [(opE e1 op e2)
     ((eval-op op) (eval-exp e1 env env-f) (eval-exp e2 env env-f))]
    [(ifzE con t f)
     (if (= 0 (eval-exp con env env-f))
                        (eval-exp t env env-f)
                        (eval-exp f env env-f))]
    [(letE sym e1 e2)
     (eval-exp e2 (extend-env env sym (eval-exp e1 env env-f)) env-f)]
    [(funE name args)
     (let ([f-pair (lookup-env-f name (map (lambda (x) (eval-exp x env env-f)) args) env-f)])
           (eval-exp (fst f-pair) (snd f-pair) env-f))]))

(define (eval-def [defs : (Listof Def)] [acc : Env-f]) : Env-f
  (if (empty? defs)
      acc
      (eval-def (rest defs) (extend-env-f acc (first defs)))))

(define (eval-program (p : Pro)) : Value
  (eval-exp (proE-body p)
            mt-env
            (eval-def (proE-definitions p) (list))))


(define (run [s : S-Exp]) : Value
  (eval-program (parse-program s)))
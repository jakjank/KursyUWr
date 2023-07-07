#lang racket
(require data/heap)
(provide sim? wire?
         (contract-out
          [make-sim        (-> sim?)]
          [sim-wait!       (-> sim? positive? void?)]
          [sim-time        (-> sim? real?)]
          [sim-add-action! (-> sim? positive? (-> any/c) void?)]

          [make-wire       (-> sim? wire?)]
          [wire-on-change! (-> wire? (-> any/c) void?)]
          [wire-value      (-> wire? boolean?)]
          [wire-set!       (-> wire? boolean? void?)]

          [bus-value (-> (listof wire?) natural?)]
          [bus-set!  (-> (listof wire?) natural? void?)]

          [gate-not  (-> wire? wire? void?)]
          [gate-and  (-> wire? wire? wire? void?)]
          [gate-nand (-> wire? wire? wire? void?)]
          [gate-or   (-> wire? wire? wire? void?)]
          [gate-nor  (-> wire? wire? wire? void?)]
          [gate-xor  (-> wire? wire? wire? void?)]

          [wire-not  (-> wire? wire?)]
          [wire-and  (-> wire? wire? wire?)]
          [wire-nand (-> wire? wire? wire?)]
          [wire-or   (-> wire? wire? wire?)]
          [wire-nor  (-> wire? wire? wire?)]
          [wire-xor  (-> wire? wire? wire?)]

          [flip-flop (-> wire? wire? wire? void?)]))

;structs-----------------------------------
(struct sim ([time] [act-h]) #:mutable #:transparent)
(struct wire ([value] [actions] [sim]) #:mutable #:transparent)
(struct action ([function] [time]))

;sim stuff---------------------------------
(define (action<= a b)
  (<= (action-time a) (action-time b)))

(define (make-sim)
  (sim 0 (make-heap action<=)))

(define (sim-wait! simulation time)
  (define action-q (sim-act-h simulation))
  (define current-time (sim-time simulation))
  (cond [(= (heap-count action-q) 0)
         (set-sim-time! simulation (+ current-time time))]
        [else
         (define next-action (heap-min action-q))
         (define time-to-next-action (- (action-time next-action) current-time))
         (cond [(<= time-to-next-action time)
                (define remaining-time (- time time-to-next-action))
                (set-sim-time! simulation (action-time next-action))
                ((action-function next-action))
                (heap-remove-min! action-q)
                (sim-wait! simulation remaining-time)]
               [else
                (set-sim-time! simulation (+ current-time time))])]))

(define (sim-add-action! simulation delay function)
  (let* ([act-time (+ delay (sim-time simulation))]
         [new-act (action function act-time)])
    (heap-add! (sim-act-h simulation) new-act)))

;wire stuff-----------------------------------
(define (make-wire simulation)
  (wire #f '() simulation))

(define (wire-on-change! wire function)
  (set-wire-actions! wire (cons function (wire-actions wire)))
  (function))

(define (wire-set! wire boolean)
  (define (call-actions xs)
    (if (null? xs)
        (void)
        (begin
          ((car xs))
          (call-actions (cdr xs)))))
  (if (eq? (wire-value wire) boolean)
      (void)
      (begin
        (set-wire-value! wire boolean)
        (call-actions (wire-actions wire)))))

;gates--------------------------------------
(define (gate-not wire1 wire2)
  (let* ([simulation (wire-sim wire1)]
         [not-action (lambda () (wire-set! wire1 (not (wire-value wire2))))])
    (wire-on-change! wire2 (lambda () (sim-add-action! simulation 1 not-action)))))

(define (supreme-gate output in1 in2 f delay symbol)
  (let ([simulation (wire-sim in1)])
    (let ([action (lambda () (wire-set! output (f (wire-value in1) (wire-value in2))))])
      (begin
        (wire-on-change! in1 (lambda () (sim-add-action! simulation delay action)))
        (wire-on-change! in2 (lambda () (sim-add-action! simulation delay action)))))))
            
(define (gate-and output in1 in2)
  (supreme-gate output in1 in2 (lambda (x y) (and x y)) 1 'gate-and))

(define (gate-nand output in1 in2)
  (supreme-gate output in1 in2 (lambda (x y) (nand x y)) 1 'gate-nand))

(define (gate-or output in1 in2)
  (supreme-gate output in1 in2 (lambda (x y) (or x y)) 1 'gate-or))

(define (gate-nor output in1 in2)
  (supreme-gate output in1 in2 (lambda (x y) (nor x y)) 1 'gate-nor))

(define (gate-xor output in1 in2)
  (supreme-gate output in1 in2 (lambda (x y) (xor x y)) 2 'gate-xor))

;wire stuff----------------------------------------
(define (wire-not input)
  (let* ([simulation (wire-sim input)]
         [output (make-wire simulation)]
         [not-action (lambda () (wire-set! output (not (wire-value input))))])
    (begin
      (wire-on-change! input (lambda () (sim-add-action! simulation 1 not-action)))
      output)))

(define (supreme-wire in1 in2 f delay symbol)
  (let* ([simulation (wire-sim in1)]
         [output (make-wire simulation)]
         [action (lambda () (wire-set! output (f (wire-value in1) (wire-value in2))))])
    (begin
      (wire-on-change! in1 (lambda () (sim-add-action! simulation delay action)))
      (wire-on-change! in2 (lambda () (sim-add-action! simulation delay action)))
      output)))

(define (wire-and in1 in2)
  (supreme-wire in1 in2 (lambda (x y) (and x y)) 1 'wire-and))

(define (wire-nand in1 in2)
  (supreme-wire in1 in2 (lambda (x y) (nand x y)) 1 'wire-nand))

(define (wire-or in1 in2)
  (supreme-wire in1 in2 (lambda (x y) (or x y)) 1 'wire-or))

(define (wire-nor in1 in2)
  (supreme-wire in1 in2 (lambda (x y) (nor x y)) 1 'wire-nor))

(define (wire-xor in1 in2)
  (supreme-wire in1 in2 (lambda (x y) (xor x y)) 2 'wire-xor))

(define (bus-set! wires value)
  (match wires
    ['() (void)]
    [(cons w wires)
     (begin
       (wire-set! w (= (modulo value 2) 1))
       (bus-set! wires (quotient value 2)))]))

(define (bus-value ws)
  (foldr (lambda (w value) (+ (if (wire-value w) 1 0) (* 2 value)))
         0
         ws))

(define (flip-flop out clk data)
  (define sim (wire-sim data))
  (define w1  (make-wire sim))
  (define w2  (make-wire sim))
  (define w3  (wire-nand (wire-and w1 clk) w2))
  (gate-nand w1 clk (wire-nand w2 w1))
  (gate-nand w2 w3 data)
  (gate-nand out w1 (wire-nand out w3)))
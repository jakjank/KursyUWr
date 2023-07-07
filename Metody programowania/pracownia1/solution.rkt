#lang racket

(require rackunit)

(provide (struct-out column-info)
         (struct-out table)
         (struct-out and-f)
         (struct-out or-f)
         (struct-out not-f)
         (struct-out eq-f)
         (struct-out eq2-f)
         (struct-out lt-f)
         table-insert
         table-project
         table-sort
         table-select
         table-rename
         table-cross-join
         table-natural-join)

(define-struct column-info (name type) #:transparent)

(define-struct table (schema rows) #:transparent)

(define cities
  (table
   (list (column-info 'city    'string)
         (column-info 'country 'string)
         (column-info 'area    'number)
         (column-info 'capital 'boolean))
   (list (list "Wrocław" "Poland"  293 #f)
         (list "Warsaw"  "Poland"  517 #t)
         (list "Poznań"  "Poland"  262 #f)
         (list "Berlin"  "Germany" 892 #t)
         (list "Munich"  "Germany" 310 #f)
         (list "Paris"   "France"  105 #t)
         (list "Rennes"  "France"   50 #f))))

(define countries
  (table
   (list (column-info 'country 'string)
         (column-info 'population 'number))
   (list (list "Poland" 38)
         (list "Germany" 83)
         (list "France" 67)
         (list "Spain" 47))))

(define (empty-table columns) (table columns '()))

; Wstawianie

;zwraca zapytanie o typ (dostaje nazwe typu)
(define (what-type s)
  (cond [(equal? s 'string) string?]
        [(equal? s 'number) number?]
        [(equal? s 'symbol) symbol?]
        [else boolean?]))

;sprawdza czy w wierszu typy zgadzaja sie ze schematem
(define (type-correctness row schema)
  (if (empty? schema)
      #t
      (if ((what-type (column-info-type (car schema))) (car row))
          (type-correctness (cdr row) (cdr schema))
          #f)))

(define (table-insert row tab)
  (if (= (length row) (length (table-schema tab)))
      (if (type-correctness row (table-schema tab))
          (table
           (table-schema tab)
           (cons row (table-rows tab)))
          (error "elementy nie sa wlasciwych typow"))
      (error "niewlasciwa liczba kolumn"))  
  )

; Projekcja

;zwraca typ column-info z scheme o nazwach jak w cols
(define (get-schema cols schema acc whole-schema)
  (if (empty? cols)
      (reverse acc)
      (if (empty? schema)
          (get-schema cols whole-schema acc whole-schema)
          (if (equal? (column-info-name (car schema)) (car cols))
              (get-schema (cdr cols) (cdr schema) (cons (car schema) acc) whole-schema)
              (get-schema cols (cdr schema) acc whole-schema)))))

;zweaca liste numerow kolumn na ktorych sa te z tmp-scheme na scheme
(define (which-columns tmp-schema schema numOfCol acc whole-schema)
  (if (empty? tmp-schema)
       (reverse numOfCol)
       (if (empty? schema)
           (which-columns tmp-schema whole-schema numOfCol 0 whole-schema)
           (if (equal? (column-info-name (car tmp-schema)) (column-info-name (car schema)))
               (which-columns (cdr tmp-schema) (cdr schema) (cons acc numOfCol) (+ acc 1) whole-schema)
               (which-columns tmp-schema (cdr schema) numOfCol (+ acc 1) whole-schema)))))

;zwraca wiersz o elementach na wybranych indeksach z row
(define (get-row row new-row numOfCol)
  (if (empty? numOfCol)
      (reverse new-row)
      (get-row row (cons (list-ref row (car numOfCol)) new-row) (cdr numOfCol))))

;zwraca wiersze o elementach na wybranych indeksach z rows
(define (get-rows rows new-rows numOfCol)
  (if (empty? rows)
      (reverse new-rows)
      (get-rows (cdr rows) (cons (get-row (car rows) '() numOfCol) new-rows) numOfCol)))

(define (table-project cols tab)
  (define tmp-schema (get-schema cols (table-schema tab) '() (table-schema tab)))
  (define tmp-numOfCol (which-columns tmp-schema (table-schema tab) '() 0 (table-schema tab)))
  (define tmp-rows (get-rows (table-rows tab) '() tmp-numOfCol))
  (table
   tmp-schema
   tmp-rows))


; Sortowanie

;porownuje dowolne typy
(define (compare a b)
  (cond [(string? a) (string<? a b)]
        [(symbol? a) (symbol<? a b)]
        [(number? a) (< a b)]
        [else (if  (and (equal? a #f) (equal? b #t))
                   #t
                   #f)]))
;wklada element w kolejnosci wzgl. kolumny do rows
(define (insert num-of-col rows elem)
  (if (empty? rows)
      (cons elem null)
      (if (compare (list-ref elem num-of-col) (list-ref (car rows) num-of-col))
          (cons elem rows)
          (cons (car rows) (insert num-of-col (cdr rows) elem)))))

;insertion sort wzgl. kolumny o danym numerze
(define (sorting-rows rows num-of-col)
  (define (it rows new-rows num-of-col)
    (if (empty? rows)
        new-rows
        (it (cdr rows) (insert num-of-col new-rows (car rows)) num-of-col)))
  (it rows '() num-of-col))

(define (table-sort cols tab)
  (define order-of-sort(which-columns
                        (get-schema cols (table-schema tab) '() (table-schema tab))
                        (table-schema tab)
                        '()
                        0
                        (table-schema tab)))
  (define (it order-of-sort rows)
    (if (empty? order-of-sort)
        rows
        (it (cdr order-of-sort) (sorting-rows rows (car order-of-sort)))))
  (table
   (table-schema tab)
   (it (reverse order-of-sort) (table-rows tab))))


; Selekcja

(define-struct and-f (l r))
(define-struct or-f (l r))
(define-struct not-f (e))
(define-struct eq-f (name val))
(define-struct eq2-f (name name2))
(define-struct lt-f (name val))

(define (rows-repeating tab1 tab2)
  (define new-table (table (table-schema tab1) '()))
  (define (add-repeating-rows to-table rows1 rows2)
    (if (empty? rows1)
        to-table
        (if (row-in-rows? rows2 (car rows1))
            (add-repeating-rows (table-insert (car rows1) to-table) (cdr rows1) rows2)
            (add-repeating-rows to-table (cdr rows1) rows2))))
  (add-repeating-rows new-table (table-rows tab1) (table-rows tab2)))

(define (rows-from-both tab1 tab2)
  (define new-table (table (table-schema tab1) '()))
  (define (add-all-rows to-table from-rows)
    (if (empty? from-rows)
        to-table
        (add-all-rows (table-insert (car from-rows) to-table) (cdr from-rows))))
  (add-all-rows (add-all-rows new-table (table-rows tab1)) (table-rows tab2)))

(define (row-in-rows? rows row)
    (if (empty? rows)
        #f
        (if (equal? (car rows) row)
            #t
            (row-in-rows? (cdr rows) row))))

(define (rows-left new-tab tab)
  (define (it rows new-rows result)
    (if (empty? rows)
        result
        (if (row-in-rows? new-rows (car rows))
            (it (cdr rows) new-rows result)
            (it (cdr rows) new-rows (cons (car rows) result)))))
  (table
   (table-schema tab)
   (it (table-rows tab) (table-rows new-tab) '())))

(define (rows-col-as-val tab name val)
  (define name-num (car (which-columns
                           (get-schema (cons name null) (table-schema tab) '() (table-schema tab))
                           (table-schema tab)
                           '()
                           0
                           (table-schema tab))))
  (define (it rows new-rows num val)
    (if (empty? rows)
        (reverse new-rows)
        (if (equal? (list-ref (car rows) num) val)
            (it (cdr rows) (cons (car rows) new-rows) num val)
            (it (cdr rows) new-rows num val))))
  (table
   (table-schema tab)
   (it (table-rows tab) '() name-num val)))

  
(define (rows-as-rows tab name1 name2)
  (define name1-num (car (which-columns
                           (get-schema (cons name1 null) (table-schema tab) '() (table-schema tab))
                           (table-schema tab)
                           '()
                           0
                           (table-schema tab))))
  (define name2-num (car (which-columns
                           (get-schema (cons name2 null) (table-schema tab) '() (table-schema tab))
                           (table-schema tab)
                           '()
                           0
                           (table-schema tab))))
  (define (it rows new-rows num1 num2)
    (if (empty? rows)
        (reverse new-rows)
        (if (equal? (list-ref (car rows) num1) (list-ref (car rows) num2))
            (it (cdr rows) (cons (car rows) new-rows) num1 num2)
            (it (cdr rows) new-rows num1 num2))))
  (table
   (table-schema tab)
   (it (table-rows tab) '() name1-num name2-num)))

  
(define (rows-col-smaller-than tab col val)
  (define sorted-rows (table-rows (table-sort (cons col null) tab)))
  (define num-of-col (car (which-columns
                           (get-schema (cons col null) (table-schema tab) '() (table-schema tab))
                           (table-schema tab)
                           '()
                           0
                           (table-schema tab))))
  (define (it sorted-rows num-of-col val new-rows)
    (if (empty? sorted-rows)
        (reverse new-rows)
        (if (compare (list-ref (car sorted-rows) num-of-col) val)
            (it (cdr sorted-rows) num-of-col val (cons (car sorted-rows) new-rows))
            (reverse new-rows))))
  (table
   (table-schema tab)
   (it sorted-rows num-of-col val '())))

(define (select-rows tab form)
  (cond [(and-f? form) (rows-repeating
                        (select-rows tab (and-f-l form))
                        (select-rows tab (and-f-r form)))]
        [(or-f? form)  (rows-from-both
                        (select-rows tab (or-f-l form))
                        (select-rows tab (or-f-r form)))]
        [(not-f? form) (rows-left
                        (select-rows tab (not-f-e form))
                        tab)]
        [(eq-f? form)  (rows-col-as-val
                        tab
                        (eq-f-name form)
                        (eq-f-val form))]
        [(eq2-f? form) (rows-as-rows
                        tab
                        (eq2-f-name form)
                        (eq2-f-name2 form))]
        [else (rows-col-smaller-than
               tab
               (lt-f-name form)
               (lt-f-val form))]))

(define (table-select form tab)
  (table
   (table-schema tab)
   (table-rows (select-rows tab form))))

; Zmiana nazwy

(define (table-rename col ncol tab)
  (define (change-name-of-col col ncol tmp-schema)
    (if (equal? (column-info-name (car tmp-schema)) col)
        (cons (column-info ncol (column-info-type (car tmp-schema)))
              (cdr tmp-schema))
        (cons (car tmp-schema)
              (change-name-of-col col ncol (cdr tmp-schema)))))
  (table
   (change-name-of-col col ncol (table-schema tab))
   (table-rows tab)))
  

; Złączenie kartezjańskie 

(define (table-cross-join tab1 tab2)
  (define expanded-schema (append (table-schema tab1) (table-schema tab2)))
  (define new-table (table expanded-schema '()))
  (define (it new-table rows1 rows2 all-rows2)
    (if (empty? rows1)
        new-table
        (if (empty? rows2)
            (it
             new-table
             (cdr rows1)
             all-rows2
             all-rows2)
            (it
             (table-insert (append (car rows1) (car rows2)) new-table)
             rows1
             (cdr rows2)
             all-rows2))))
  (it new-table (table-rows tab1) (table-rows tab2) (table-rows tab2)))
  

; Złączenie

(define (table-natural-join tab1 tab2)
  (define (get-common-columns schema1 schema2 whole-schema2 result)
    (cond [(empty? schema1) (reverse result)]
          [(empty? schema2) (get-common-columns (cdr schema1) whole-schema2 whole-schema2 result)]
          [(equal? (column-info-name (car schema1))
                   (column-info-name (car schema2)))
           (get-common-columns (cdr schema1) whole-schema2 whole-schema2 (cons (car schema1) result))]
          [else (get-common-columns schema1 (cdr schema2) whole-schema2 result)]))
  
  (define common-columns (get-common-columns
                         (table-schema tab1)
                         (table-schema tab2)
                         (table-schema tab2)
                         '()))

  (define (get-2-tail sym)
    (string->symbol (string-append (symbol->string sym) "2")))
  
  (define (change-name-table columns tab)
    (if (empty? columns)
        tab
        (change-name-table
         (cdr columns)
         (table-rename (column-info-name (car columns)) (get-2-tail (column-info-name (car columns))) tab))))

  (define renamed-tab2 (change-name-table common-columns tab2))
  
  (define cross-joined-table (table-cross-join tab1 renamed-tab2))

  (define (delete-rows common-columns table)
    (if (empty? common-columns)
        table
        (delete-rows (cdr common-columns) (table-select
                                           (eq2-f (column-info-name (car common-columns))
                                                  (get-2-tail (column-info-name (car common-columns))))
                                           table))))

  (define (rid-of-columns schema columns whole-columns result)
    (cond [(empty? schema) (reverse result)]
          [(empty? columns) (rid-of-columns (cdr schema) whole-columns whole-columns (cons (column-info-name (car schema)) result))]
          [(equal? (get-2-tail (column-info-name (car columns))) (column-info-name (car schema)))
           (rid-of-columns (cdr schema) whole-columns whole-columns result)]
          [else (rid-of-columns schema (cdr columns) whole-columns result)]))


  (table-project
   (rid-of-columns (table-schema cross-joined-table) common-columns common-columns '())
   (delete-rows common-columns cross-joined-table))
)


  







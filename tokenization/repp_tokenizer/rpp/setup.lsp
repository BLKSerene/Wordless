(in-package :lkb)

;;;
;;; Copyright (c) 2009 -- 2018 Stephan Oepen (oe@ifi.uio.no); 
;;; see `LICENSE' for conditions.
;;;


(clear-repp)

;;;
;;; as of September 2008, REPP supports `ensembles' of rule sets, where select
;;; modules (XML or LaTeX markup normalization, for example) can be activated
;;; in the REPP environment or top-level repp() call.  by default, turn on the
;;; XML and ASCII modules.
;;;
(read-repp (lkb-pathname (parent-directory "rpp") "xml.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "latex.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "ascii.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "html.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "wiki.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "lgt.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "gml.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "robustness.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "quotes.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "ptb.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "lkb.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "micro.rpp"))
(read-repp (lkb-pathname (parent-directory "rpp") "tokenizer.rpp"))
(setf *repp-calls* '(:xml :lgt :ascii :quotes))
(setf *repp-characterize-p* t)
(setf *repp-characterization-beam* 2)
(setf *repp-interactive* '(:tokenizer :xml :lgt :ascii :quotes :lkb))
(setf *repp-debug-p* nil)

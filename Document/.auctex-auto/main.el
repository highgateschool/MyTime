(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "a4paper" "total={6in, 8in}") ("inputenc" "utf8")))
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "geometry"
    "graphicx"
    "listings"
    "xcolor"
    "float"
    "inputenc")
   (LaTeX-add-labels
    "fig:forest1"
    "fig:evernote1"
    "fig:todoist1"
    "fig:rtm1"
    "fig:ike1"
    "fig:keep1"
    "fig:trello1"
    "windows"
    "operating-systems-32-bit-and-64-bit"
    "recommended-hardware"
    "mac"
    "operating-systems"
    "recommended-hardware_1"
    "gnulinux"
    "software-requirements"
    "fig:TDD1"
    "fig:task_index_mockup"
    "fig:event_index_mockup"
    "fig:schedule_mockup"
    "fig:task_detail_mockup"
    "fig:event_detail_mockup"
    "fig:work_space_mockup"
    "fig:statistics_mockup"
    "fig:database1"
    "fig:task_index1"
    "fig:task_detail1"
    "fig:task_form1")
   (LaTeX-add-index-entries
    "\\item"))
 :latex)


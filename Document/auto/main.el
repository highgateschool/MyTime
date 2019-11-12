(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "a4paper" "total={6in, 8in}")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "graphicx"
    "geometry")
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
    "fig:TDD1")
   (LaTeX-add-index-entries
    "\\item"))
 :latex)


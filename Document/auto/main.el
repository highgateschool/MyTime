(TeX-add-style-hook
 "main"
 (lambda ()
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "graphicx")
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
    "software-requirements")
   (LaTeX-add-index-entries
    "\\item"))
 :latex)


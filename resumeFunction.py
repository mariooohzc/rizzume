# must end document afterwards
# remember to do that


def heading(name, phone, email, linkedin, titles):
    """
    creates the heading section for the resume

    Parameters
    ----------
    name: string
    phone: string
    email: string
    linkedin: string

    Returns
    -------
    string
        return LaTeX code for the heading section
    """
    x = r"\begin{center}" + "\n"
    x += r"\textbf{\Huge \scshape " + name + r"} \\ \vspace{1pt}" + "\n"
    x += r"\small " + phone + r" $|$ {\underline{" + email + r"}} $|$ " + "\n"
    x += r"{\underline{" + linkedin + "}}"

    if len(titles):
        for title in titles:
            if title:
                x += r" $|$ {\underline{" + title + "}}"

    x += r"\end{center}"
    x += "\n\n\n"
    return x


def education(universityName, country, degree, major, startDate, endDate, *extra):
    education = list()
    education.append(r"\section{Education}")
    education.append(r"\resumeSubHeadingListStart")
    education.append(r"\resumeSubheading")
    education.append(r"{" + universityName + r"}" + "{" + country + "}")
    education.append(
        r"{" + degree + "in" + major + r"}" + r"{" + startDate + " -- " + endDate + "}"
    )

    repetitions = len(extra) % 6
    for i in range(1, repetitions + 1):
        education.append(r"\resumeSubHeadingListStart")
        education.append(r"\resumeSubheading")
        education.append(r"{" + extra[0 * i] + r"}" + "{" + extra[1 * i] + "}")
        education.append(
            r"{"
            + extra[2 * i]
            + "in"
            + extra[3 * i]
            + r"}"
            + r"{"
            + extra[4 * i]
            + " -- "
            + extra[5 * i]
            + "}"
        )
    education.append(r"\resumeSubHeadingListEnd\n\n\n")

    return "\n".join(education)

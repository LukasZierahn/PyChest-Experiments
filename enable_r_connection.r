if(!require("Rserve")){
    print("trying to install Rserve")
    install.packages("Rserve")
    if(!require("Rserve")){
      stop("Rserve could not be installed")
    }
}

if(!require("wbs")){
    print("trying to install wbs")
    install.packages("wbs")
    if(!require("wbs")){
      stop("wbs could not be installed")
    }
}

Rserve()

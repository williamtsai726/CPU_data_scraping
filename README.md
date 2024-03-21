This is a file that does data scraping on https://www.computerbase.de/2023-12/intel-meteor-lake-core-ultra-7-155h-test/ to collect all the information about test benchmark on CPUs.
Below is a snippet of code that does pptx to pdf conversion:

        from spire.presentation import *
        from spire.presentation.common import *
        
        //Create a Presentation object
        presentation = Presentation()
        //Load a PowerPoint presentation in PPTX format
        presentation.LoadFromFile("filename")
        
        //Convert the presentation to PDF format
        presentation.SaveToFile("target.pdf", FileFormat.PDF)
        presentation.Dispose()

import pdfkit

def create_pdf_report(content, out_file_location):
  print("create_pdf_report start")
  try:
    options = {
        'page-size': 'Letter', 'margin-top': '0.75in', 'margin-right': '0.75in', 'margin-bottom': '0.75in', 'margin-left': '0.75in',
        'encoding': "UTF-8", 'custom-header': [('Accept-Encoding', 'gzip')], 'no-outline': None
    }

    pdfkit.from_string(content, options=options, output_path=out_file_location, verbose=True)
  except Exception as e:
    print("create_pdf_report error", e)
    raise e
  print("create_pdf_report error end")
  return True


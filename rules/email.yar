rule email_list
{
  strings:
    $email_address = /\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b/
  condition:
    #email_address > 30
}

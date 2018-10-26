rule test
{
  strings:
    $hello = "hello"
    $world = "world"
  condition:
    any of them
}

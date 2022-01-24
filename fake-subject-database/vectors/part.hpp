// You have to fill this file to answer questions of PART.

#pragma tpinf_open_only_in_subject
#pragma // write something here to avoid bad nested incusions
#pragma tpinf_close_only_in_subject


#pragma tpinf_open_answer

#pragma tpinf_Q once
#pragma once

#pragma tpinf_Q vector-header
#include <vector>


#pragma tpinf_Q Foo-struct
struct Foo {
  int val;
  
#pragma tpinf_Q Foo-default
  Foo() = default;
  
#pragma tpinf_Q Foo-int-constr
  Foo(int val);
};

#pragma tpinf_close_answer

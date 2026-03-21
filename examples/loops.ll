; ModuleID = "minilang_module"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
entry:
  %"i" = alloca i32
  store i32 0, i32* %"i"
  br label %"while.cond"
while.cond:
  %"i.1" = load i32, i32* %"i"
  %"lt" = icmp slt i32 %"i.1", 5
  %".4" = icmp ne i1 %"lt", 0
  br i1 %".4", label %"while.body", label %"while.end"
while.body:
  %".6" = bitcast [4 x i8]* @".fmt" to i8*
  %"i.2" = load i32, i32* %"i"
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", i32 %"i.2")
  %"i.3" = load i32, i32* %"i"
  %"add" = add i32 %"i.3", 1
  store i32 %"add", i32* %"i"
  br label %"while.cond"
while.end:
  %"sum" = alloca i32
  store i32 0, i32* %"sum"
  %"j" = alloca i32
  store i32 1, i32* %"j"
  br label %"while.cond.1"
while.cond.1:
  %"j.1" = load i32, i32* %"j"
  %"le" = icmp sle i32 %"j.1", 10
  %".13" = icmp ne i1 %"le", 0
  br i1 %".13", label %"while.body.1", label %"while.end.1"
while.body.1:
  %"sum.1" = load i32, i32* %"sum"
  %"j.2" = load i32, i32* %"j"
  %"add.1" = add i32 %"sum.1", %"j.2"
  store i32 %"add.1", i32* %"sum"
  %"j.3" = load i32, i32* %"j"
  %"add.2" = add i32 %"j.3", 1
  store i32 %"add.2", i32* %"j"
  br label %"while.cond.1"
while.end.1:
  %".18" = bitcast [4 x i8]* @".fmt" to i8*
  %"sum.2" = load i32, i32* %"sum"
  %".19" = call i32 (i8*, ...) @"printf"(i8* %".18", i32 %"sum.2")
  ret i32 0
}

@".fmt" = internal constant [4 x i8] c"%d\0a\00"
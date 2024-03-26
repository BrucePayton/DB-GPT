import contextlib
import  sys
import asyncio
from dbgpt.core.awel import (
    DAG, BranchOperator, MapOperator, JoinOperator,
    InputOperator, SimpleCallDataInputSource,
    is_empty_data
)

def combine_function(*args) -> int:
    """for join opetator not limit number of input variable"""
    print(f"Received {len(args)} arguments: {args}")
    for arg in args:
        if not is_empty_data(arg):
            return arg
    return None

def _temporary_variable(name, value):
    try:
        setattr(sys.modules[__name__], name, value)
        return contextlib.suppress(AttributeError)  # 返回上下文管理器
    except AttributeError:
        return contextlib.ExitStack().enter_context(contextlib.suppress(AttributeError))  # 返回上下文管理器

class TemplateOfCommonOperator(object):

    def __init__(self) -> None:
        self.task_tuple = ()

    def branch_using_dag(self, input_branch_mapping: dict, input_branch_functions: dict, input_combine_function):
        """set a basic branch using """
        with DAG("awel_branch_operator") as dag:
            input_task = InputOperator(input_source=SimpleCallDataInputSource())
            task = BranchOperator(branches=input_branch_mapping)
            join_task = JoinOperator(combine_function=input_combine_function)
            with contextlib.ExitStack() as stack:
                for func, executor_function in input_branch_functions.items(): #involve loop for functions
                    task_name = func #set string value to task name
                    stack.enter_context(_temporary_variable(func, executor_function)) #turn string value to variable value
                    func = MapOperator(task_name=task_name, map_function=executor_function) #set function value
                    input_task >> task >> func >> join_task #for loop
            return join_task





def branch_1(x: int) -> bool:
    return x == 1

def branch_2(x: int) -> bool:
    return x == 2

def branch_3(x: int) -> bool:
    return x == 3

branch_mapping = {
    branch_1: "even_task",
    branch_2: "odd_task",
    branch_3: "other_task"
}


def even_func(x: int) -> int:
    print(f"Branch even, {x} is even, multiply by 10")
    return x * 10

def odd_func(x: int) -> int:
    print(f"Branch odd, {x} is odd, multiply by itself")
    return x * x

def other_func(x: int) -> int:
    print(f"Branch other, {x} is other, print itself")
    return x

branch_functions = {
    branch_mapping[branch_1]: even_func,
    branch_mapping[branch_2]: odd_func,
    branch_mapping[branch_3]: other_func
}


object_template = TemplateOfCommonOperator()

branch_task = object_template.branch_using_dag(input_branch_mapping=branch_mapping, input_branch_functions=branch_functions, input_combine_function=combine_function)
print("First call, input is 5")
asyncio.run(branch_task.call(call_data=5))
print("=" * 80)

import angr
import claripy

def main():
  #Load the binary file
  p = angr.Project('login', auto_load_libs=False)

  #Create a symbolic bitvector for the username(8 characters) and the password
  fixed_username = b'useruser\n'   #username doesn't matter here, but it should be 8 characters
  password = claripy.BVS('password', 8*8)

  #Concatanate username and password with a newline
  input_data = claripy.Concat(claripy.BVV(fixed_username), password, claripy.BVV(b'\n'))
  state = p.factory.entry_state(stdin=input_data)
  simgr = p.factory.simulation_manager(state)
  simgr.explore(find=lambda s: b"Access granted! You are now in the admin console!" in s.posix.dumps(1))

  if simgr.found:
    found_state = simgr.found[0]

    solution = found_state.solver.eval(password, cast_to=bytes)
    print(f"Backdoor password found: {solution.decode()}")
  else:
    print("Backdoor password not found")

if __name__ == "__main__":
   main()
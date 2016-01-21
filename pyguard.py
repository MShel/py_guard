#!/usr/bin/env python
import sys, getopt, subprocess
import os

sys.path.insert(0, os.getcwd())

# Get the args
def main(argv):
    # Clear the screen
    subprocess.call('clear', shell=True)
    try:
        opts, args = getopt.getopt(argv, 'h', ['email=', 'dblevel='])
        '''
         options:
          --email=test@test.com .. you should have mail server setup
          --dblevel=20 noise level
         '''
  
        
        for opt, arg in opts:
            if opt in ('--help', '-h'):
                print('HEEELLP')
                sys.exit(0)
            
            if opt == '--email' and is_email(arg) == true:
                email = arg
            
            if opt == '--dblevel':
                db_level = arg

                
        '''
        need to spin the threds andd get all the juzz up and running
        '''
        
    except getopt.GetoptError:
        sys.exit(2)
    except PermissionError:
        sys.exit(2)
    except Exception as e:
        print(e)
        sys.exit(2)
    except IndexError:
        sys.exit(2)
    except KeyboardInterrupt:
        sys.exit(1)
    except ImportError:
        sys.exit(2)    
        
if __name__ == "__main__":
    main(sys.argv[1:])

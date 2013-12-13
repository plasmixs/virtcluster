
/*Autogenerated file*/

#include "_proto.h"
#include "../../../../src/utLib/inc/_smod.h"

void sigHndlr (int signum);
genErr_t raisesignal (void);

int sig_test_var = false;
void
sigHndlr (int signum)
{
  (void)signum;
  sig_test_var = true;
}

genErr_t raisesignal (void)
{				/*raise a sigusr1. */
  raise (SIGUSR1);
  if (sig_test_var == true)
    return SUCCESS;
  else
    return FAILURE;
}

void
test_smod (void)
{

  bs_smodCls sObj = NULL;

  hdr ("Testing of smod module started");

  retVal = bs_smodInit (&sObj, iMObj);
  EXEC_TSTCASE (&tstCase, " Initialize the signal module ", retVal, retVal,
		ec2ES (retVal), 0);

  retVal = bs_registerHandler (sObj, SIGUSR1, &sigHndlr, 0);
  EXEC_TSTCASE (&tstCase, " Register a signal handler and verify signal ",
		retVal, retVal, ec2ES (retVal), 0);

  retVal = raisesignal ();
  EXEC_TSTCASE (&tstCase, " Raise a signal and check handler ", retVal,
		retVal, ec2ES (retVal), 0);

  retVal = bs_smodFin (&sObj, iMObj);
  EXEC_TSTCASE (&tstCase, " Finalise the signal module ", retVal, retVal,
		ec2ES (retVal), 0);

  hdr ("Testing of smod module compleated");
}

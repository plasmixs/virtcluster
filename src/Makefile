#############################################################################
# Makefile                                                                  #
#############################################################################

target:$(MODULE)

.PHONY:utLib
utLib:
	$(MAKE) -C ./utLib/ $(TARGET)

.PHONY:commision
commision:
	$(MAKE) -C ./commision/ $(TARGET)

.PHONY:cpackgen
cpackgen:
	$(MAKE) -C ./cpackgen/ all TARGET=$(TARGET)

all:utLib commision cpackgen

##############################################################################

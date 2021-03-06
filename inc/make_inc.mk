#############################################################################
# Makefile                                                                  #
#############################################################################

include $(CURR_DIR)/conf/config.mk

CFLAGS := $(CFLAGS)\
	 -Wall -Wextra -Wswitch-enum -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations\
	 $(DEBUG_FLAG) $(PROD_FLAG) $(GCONF_FLAGS) $(GPROF_FLAGS)

LFLAGS := $(LFLAGS) $(LDFLAGS)\
	 -Wall -Wextra -Wswitch-enum -Wstrict-prototypes -Wmissing-prototypes -Wmissing-declarations\
	 $(DEBUG_FLAG) $(PROD_FLAG)

SH_LIB_CFLAGS := -fPIC
SH_LIB_LFLAGS := -shared

LD := $(CC)
ARFLAGS := cr
OBJ_DIR := ./obj
BIN_DIR := ./bin
LIB_DIR := ./lib
STATIC_LIB_DIR := $(LIB_DIR)/static
INC_DIR := ./inc
SRC_DIR := ./src
BLD_DIR := ./bld
_RPM_DIR := ./bld/rpm
RPM_DIR := $(_RPM_DIR)/$(ARCH)
COM_INC_DIR := $(CURR_DIR)/src/com_inc
COM_LIB_DIR := $(CURR_DIR)/src/com_lib
CONFIG_DIR := $(CURR_DIR)/conf
CONFIG_INC_DIR := $(CURR_DIR)/inc
COM_STATIC_LIB_DIR := $(COM_LIB_DIR)/static
INCLUDE = -I$(CONFIG_DIR) -I$(CONFIG_INC_DIR) -I$(COM_INC_DIR) -I$(INC_DIR)
DEFINES =

SCRIPTS_DIR := $(CURR_DIR)/scripts

#Command to list source files.
OF_CMD := find . -iname "*.c" -exec basename {} \;|xargs

COMPILE.o = $(CC) $(CFLAGS) $(INCLUDE) $(DEFINES) -MMD -MT $@ -c
LINK.exe = $(LD) $(LFLAGS) $(INCLUDE) $(DEFINES)
OUTPUT.o = -o $@
OUTPUT.exe = -o $@
LIB.so = $(LD) $(LFLAGS) $(SH_LIB_LFLAGS) $(DEFINES)
OUTPUT.so = -o $@
ARCHIVE.a = $(AR) $(ARFLAGS)
OUTPUT.a = -o $@
RANLIB.a = $(RANLIB)
RLOUTPUT.a = $@

$(OBJ_DIR)/%.o: %.c
	$(COMPILE.o) $< $(OUTPUT.o)
ifeq ($(SA),yes)
	$(SCRIPTS_DIR)/sa_run.sh "$(INCLUDE)" "$(DEFINES)" "$<" "$@"
endif

%.a:
	$(ARCHIVE.a) $(OUTPUT.a) $^
	$(RANLIB.a) $(RLOUTPUT.a)
	cp -v $@ $(COM_STATIC_LIB_DIR)

%.so:
	$(LIB.so) $^ $(OUTPUT.so)
	cp -v $@ $(COM_LIB_DIR)

%.exe:
	$(LINK.exe) $^ $(LIBS) $(OUTPUT.exe)

.PHONY:kmod
kmod:
	$(MAKE) -C $(SRC_DIR) KERNEL_SRC=$(K_SRC_DIR)\
	 MOD_DIR=$(addsuffix $(subst .,,$(OBJ_DIR)), $(shell pwd))

RPM_TARGET := $(OVERRIDE_RPM_TARGET)
ifndef RPM_TARGET
	RPM_TARGET := $(ARCH)-vc-linux
endif

%.rpm:
	rpmbuild --target=$(RPM_TARGET) -bb $(BLD_DIR)/rpm.spec

.PHONY:clean
clean:
ifeq ($(KERNEL_MAKEFILE),yes)
	$(MAKE) -C $(SRC_DIR) KERNEL_SRC=$(K_SRC_DIR) clean
else
	rm -vf $(OBJ_DIR)/*.o
	rm -vf $(OBJ_DIR)/*.d
	rm -vf $(OBJ_DIR)/*.gcno
	rm -vf $(OBJ_DIR)/*.gcda
endif

.PHONY:cleanall
cleanall:
ifeq ($(KERNEL_MAKEFILE),yes)
	$(MAKE) -C $(SRC_DIR) KERNEL_SRC=$(K_SRC_DIR) clean
	rm -vrf $(OBJ_DIR)/lib
else
	rm -vf $(OBJ_DIR)/*.o
	rm -vf $(OBJ_DIR)/*.d
	rm -vf $(BIN_DIR)/*.exe
	rm -vf $(LIB_DIR)/*.so
	rm -vf $(STATIC_LIB_DIR)/*.a
	rm -vf $(OBJ_DIR)/*.gcno
	rm -vf $(OBJ_DIR)/*.gcda
	rm -vf $(OBJ_DIR)/*.sa
	rm -vf $(OBJ_DIR)/*.sa.bkp
endif
	rm -vrf $(_RPM_DIR)/*

#############################################################################

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%define _build_arch %(uname -i)
%define _python_awips_version %(grep ^ver /awips2/repo/python-awips/setup.py | cut -d '"' -f 2)
%define _python_build_loc %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#
# Python AWIPS Spec File
#
Name: awips2-python-awips
Summary: Python AWIPS Distribution
Version: %{_python_awips_version}
Release: 1%{?dist}
Group: AWIPSII
BuildRoot: %{_build_root}
BuildArch: %{_build_arch}
URL: N/A
License: N/A
Distribution: N/A
Vendor: %{_build_vendor}
Packager: %{_build_site}

AutoReq: no
Requires: awips2-python
Requires: awips2-python-numpy
Requires: awips2-python-six
Requires: awips2-python-shapely
Provides: awips2-python-awips = %{version}

Obsoletes: awips2-python-ufpy < 15.1.3-1
Obsoletes: awips2-python-dynamicserialize < 15.1.3-1
Obsoletes: awips2-python-thrift < 20080411p1-4

BuildRequires: awips2-python
BuildRequires: awips2-python-numpy

%description
Python AWIPS Site-Package

%prep
# Verify That The User Has Specified A BuildRoot.
if [ "%{_build_root}" = "" ]
then
   echo "A Build Root has not been specified."
   echo "Unable To Continue ... Terminating"
   exit 1
fi

rm -rf %{_build_root}
mkdir -p %{_build_root}
if [ -d %{_python_build_loc} ]; then
   rm -rf %{_python_build_loc}
fi
mkdir -p %{_python_build_loc}

%build
source /etc/profile.d/awips2.sh
RC=$?
if [ ${RC} -ne 0 ]; then
   exit 1
fi

AWIPS_SRC_DIR="%{_baseline_workspace}/python-awips"
cp -R ${AWIPS_SRC_DIR} %{_python_build_loc}/
RC=$?
if [ ${RC} -ne 0 ]; then
   exit 1
fi

cd %{_python_build_loc}/python-awips

pushd . > /dev/null
/awips2/python/bin/python setup.py clean
RC=$?
if [ ${RC} -ne 0 ]; then
   exit 1
fi
/awips2/python/bin/python setup.py build
RC=$?
if [ ${RC} -ne 0 ]; then
   exit 1
fi
popd > /dev/null

%install
AWIPS_SRC_DIR="%{_baseline_workspace}/python-awips"

pushd . > /dev/null
cd %{_python_build_loc}/python-awips
export LD_LIBRARY_PATH=/awips2/python/lib
/awips2/python/bin/python setup.py install \
   --root=%{_build_root} \
   --prefix=/awips2/python
RC=$?
if [ ${RC} -ne 0 ]; then
   exit 1
fi
popd > /dev/null

%pre

%post

%preun

%postun

%clean
rm -rf %{_build_root}
rm -rf %{_python_build_loc}

%files
%defattr(644,awips,fxalpha,755)
%dir /awips2/python/lib/python3.6/site-packages
/awips2/python/lib/python3.6/site-packages/*

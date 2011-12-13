#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
# Disabled tests as pidlockfile is not anymore in the lastest python-lockfile

%define 	module	daemon
Summary:	Library to implement a well-behaved Unix daemon process
Name:		python-%{module}
Version:	1.6
Release:	1
License:	Python
Group:		Development/Languages
URL:		http://pypi.python.org/pypi/python-daemon/
Source0:	http://pypi.python.org/packages/source/p/python-daemon/%{name}-%{version}.tar.gz
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	python-lockfile
BuildRequires:	python-minimock
%endif
Requires:	python-lockfile
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library implements the well-behaved daemon specification of PEP
3143, "Standard daemon process library".

%prep
%setup -q

%{__sed} -i -e '/^#!\//, 1d' daemon/version/version_info.py

%build
%{__python} setup.py build

# Test suite requires minimock and lockfile
%if %{with tests}
PYTHONPATH=$(pwd) nosetests
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%{__rm} -rf $RPM_BUILD_ROOT%{py_sitescriptdir}/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.PSF-2
%dir %{py_sitescriptdir}/daemon
%dir %{py_sitescriptdir}/daemon/version
%{py_sitescriptdir}/daemon/*.py[co]
%{py_sitescriptdir}/daemon/version/*.py[co]
%{py_sitescriptdir}/python_daemon-%{version}-py%{py_ver}.egg-info

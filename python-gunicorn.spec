#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define	module gunicorn
Summary:	Python WSGI application server
Name:		python-%{module}
Version:	18.0
Release:	1
License:	MIT
Group:		Daemons
URL:		http://gunicorn.org/
Source0:	http://pypi.python.org/packages/source/g/%{module}/%{module}-%{version}.tar.gz
# distro-specific, not upstreamable
Patch100:	%{name}-dev-log.patch
Requires:	python-setuptools
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It
uses the pre-fork worker model, ported from Ruby's Unicorn project. It
supports WSGI, Django, and Paster applications.

%package -n python3-%{module}
Summary:	Python WSGI application server
Group:		Libraries/Python
Requires:	python3-setuptools

%description -n python3-%{module}
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It
uses the pre-fork worker model, ported from Ruby's Unicorn project. It
supports WSGI, Django, and Paster applications.

%prep
%setup -qc
mv %{module}-%{version} py2
cd py2
%patch100 -p1
cd -

%if %{with python3}
cp -a py2 py3
%endif

%build
%if %{with python2}
cd py2
%{__python} setup.py build
cd -
%endif

%if %{with python3}
cd py3
%{__python3} setup.py build
%endif

%if %{with tests}
cd py2
%{__python} setup.py test
cd -

%if %{with python3}
cd py3
%{__python3} setup.py test
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
cd py3
%{__python3} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

# rename executables in %{_bindir} so they don't collide
for executable in %{module} %{module}_django %{module}_paster; do
	mv $RPM_BUILD_ROOT%{_bindir}/{,python3-}$executable
done
cd -
%endif

%if %{with python2}
cd py2
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc py2/{LICENSE,NOTICE,README.rst,THANKS}
%attr(755,root,root) %{_bindir}/%{module}
%attr(755,root,root) %{_bindir}/%{module}_django
%attr(755,root,root) %{_bindir}/%{module}_paster
%{py_sitescriptdir}/gunicorn
%{py_sitescriptdir}/gunicorn-%{version}0-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc py3/{LICENSE,NOTICE,README.rst,THANKS}
%attr(755,root,root) %{_bindir}/python3-%{module}
%attr(755,root,root) %{_bindir}/python3-%{module}_django
%attr(755,root,root) %{_bindir}/python3-%{module}_paster
%{py3_sitescriptdir}/gunicorn
%{py3_sitescriptdir}/gunicorn-%{version}-py*.egg-info
%endif

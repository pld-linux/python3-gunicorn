#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
%bcond_without	tests	# unit tests

%define	module gunicorn
Summary:	Python WSGI application server
Summary(pl.UTF-8):	Pythonowy serwer aplikacji WSGI
Name:		python-%{module}
Version:	19.7.0
Release:	3
License:	MIT
Group:		Daemons
#Source0Download: https://pypi.python.org/simple/gunicorn
Source0:	https://files.pythonhosted.org/packages/source/g/gunicorn/%{module}-%{version}.tar.gz
# Source0-md5:	1a0eef597a5bd55f24086b2597111c94
# distro-specific, not upstreamable
Patch100:	%{name}-dev-log.patch
URL:		http://gunicorn.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-pytest >= 3.0.5
BuildRequires:	python-pytest-cov >= 2.4.0
%if "%{py_ver}" < "2.7"
BuildRequires:	python-unittest2
%endif
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest >= 3.0.5
BuildRequires:	python3-pytest-cov >= 2.4.0
%if "%{py3_ver}" < "3.3"
BuildRequires:	python-mock
%endif
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg
BuildRequires:	python3-sphinx_rtd_theme
%endif
Requires:	python-setuptools
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It
uses the pre-fork worker model, ported from Ruby's Unicorn project. It
supports WSGI, Django, and Paster applications.

%description -l pl.UTF-8
Gunicorn ("Green Unicorn" - zielony jednorożec) to pythonowy serwer
HTTP WSGI dla systemów uniksowych. Wykorzystuje model pre-fork,
przeniesiony z projektu Unicorn napisanego w języku Ruby. Obsługuje
aplikacje WSGI, Django i Paster.

%package -n python3-%{module}
Summary:	Python WSGI application server
Summary(pl.UTF-8):	Pythonowy serwer aplikacji WSGI
Group:		Libraries/Python
Requires:	python3-setuptools

%description -n python3-%{module}
Gunicorn ("Green Unicorn") is a Python WSGI HTTP server for UNIX. It
uses the pre-fork worker model, ported from Ruby's Unicorn project. It
supports WSGI, Django, and Paster applications.

%description -n python3-%{module} -l pl.UTF-8
Gunicorn ("Green Unicorn" - zielony jednorożec) to pythonowy serwer
HTTP WSGI dla systemów uniksowych. Wykorzystuje model pre-fork,
przeniesiony z projektu Unicorn napisanego w języku Ruby. Obsługuje
aplikacje WSGI, Django i Paster.

%prep
%setup -q -n %{module}-%{version}
%patch100 -p1

%{__sed} -i -e 's/==/>=/' requirements_test.txt

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

# rename executables in %{_bindir} so they don't collide
for executable in gunicorn gunicorn_paster; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/{,python3-}$executable
done
%endif

%if %{with python2}
%py_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE NOTICE README.rst THANKS
%attr(755,root,root) %{_bindir}/gunicorn
%attr(755,root,root) %{_bindir}/gunicorn_paster
%{py_sitescriptdir}/gunicorn
%{py_sitescriptdir}/gunicorn-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc LICENSE NOTICE README.rst THANKS
%attr(755,root,root) %{_bindir}/python3-gunicorn
%attr(755,root,root) %{_bindir}/python3-gunicorn_paster
%{py3_sitescriptdir}/gunicorn
%{py3_sitescriptdir}/gunicorn-%{version}-py*.egg-info
%endif

#
# Conditional build:
%bcond_without	tests	# unit tests

%define	module gunicorn
Summary:	Python WSGI application server
Summary(pl.UTF-8):	Pythonowy serwer aplikacji WSGI
Name:		python3-%{module}
Version:	20.0.4
Release:	2
License:	MIT
Group:		Daemons
#Source0Download: https://pypi.python.org/simple/gunicorn
Source0:	https://files.pythonhosted.org/packages/source/g/gunicorn/%{module}-%{version}.tar.gz
# Source0-md5:	543669fcbb5739ee2af77184c5e571a1
# distro-specific, not upstreamable
Patch100:	%{name}-dev-log.patch
URL:		https://gunicorn.org/
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools >= 3.0
%if %{with tests}
BuildRequires:	python3-aiohttp
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-pytest >= 3.2.5
BuildRequires:	python3-pytest-cov >= 2.5.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg-3
BuildRequires:	python3-sphinx_rtd_theme
%endif
Requires:	python3-setuptools
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

%prep
%setup -q -n %{module}-%{version}
%patch100 -p1

%build
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTEST_PLUGINS="pytest_cov.plugin"

%py3_build %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{gunicorn,gunicorn-3}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NOTICE README.rst THANKS
%attr(755,root,root) %{_bindir}/gunicorn-3
%{py3_sitescriptdir}/gunicorn
%{py3_sitescriptdir}/gunicorn-%{version}-py*.egg-info

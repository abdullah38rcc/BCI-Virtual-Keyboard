/* <![CDATA[ */
(function () {
    var e = null,
        f = false,
        h = window,
        i = document;

    function j(a, b) {
        return a.name = b
    }
    var k = "push",
        l = "length",
        n = "prototype",
        o = "getElementById",
        p = "offsetWidth",
        q = "tick",
        r = "start",
        t = "addEventListener",
        u = "report";
    var _B = "iphone",
        v = _B,
        w = [],
        x = h,
        z, A, B, C, D, E;

    function _G(a, b) {
        return i.defaultView.getComputedStyle(a, e).getPropertyValue(b)
    }
    var F = _G;

    function G(a) {
        if (a) {
            a.stopPropagation();
            a.preventDefault()
        }
        A && H()
    }
    var I = "a",
        J = "",
        K = "b";

    function L() {
        if (B) {
            var a, b = M();
            a = B.offsetLeft;
            if (b - a - A[p] < 5) a = b - A[p] - 5;
            A.style.left = a + "px"
        }
        B && B.setAttribute(I, J);
        A && A.setAttribute(K, J);
        C && C.setAttribute(K, J);
        C.style.height = i.height - C.offsetTop + "px";
        H = P
    }
    function P() {
        B && B.removeAttribute(I);
        A && A.removeAttribute(K);
        C && C.removeAttribute(K);
        H = L
    }
    function Q() {
        H == P && P()
    }
    function M() {
        var a = v == "android" ? 7 : 0;
        a = Math.min(x.screen.width - a, x.screen.height - a);
        if (x.innerWidth > 20) a = Math.min(a, x.innerWidth);
        return a
    }
    var H = L;
    x.og = {};
    var R = "click";
    x.og.g = function () {
        z = i[o]("og_head");
        A = i[o]("og_u");
        B = i[o]("og_r");
        C = i[o]("og_h");
        D = i[o]("og_quick");
        E = i[o]("og_z");
        if (B) {
            B.href = "javascript:0";
            i[t](R, Q, f);
            B[t](R, G, f);
            C[t](R, P, f)
        }
        for (var a; a = w.shift();) a()
    };
    x.og.tm = G;

    function S() {
        return (i.forms[0].q || J).value
    }
    function T(a, b) {
        var c = x.og.q();
        if (c) {
            var d = b ? b : a.href;
            a.href = d.replace(/([?&])q=[^&]*|$/, function (g, m) {
                return (m || "&") + "q=" + encodeURIComponent(c)
            })
        }
    }
    x.og.q = S;
    x.og.p = T;
    var V = "start";

    function W(a) {
        this.t = {};
        this.tick = function (b, c, d) {
            d = d ? d : (new Date).getTime();
            this.t[b] = [d, c]
        };
        this[q](V, e, a)
    }
    var aa = new W;
    h.gpjstiming = {
        Timer: W,
        load: aa
    };
    if (h.gpjstiming) {
        h.gpjstiming.m = {};
        h.gpjstiming.H = 1;
        var X = function (a, b, c) {
            var d = a.t[b],
                g = a.t[r];
            if (d && (g || c)) {
                d = a.t[b][0];
                g = c != undefined ? c : g[0];
                return d - g
            }
        },
            ba = function (a, b, c) {
                var d = J;
                if (a.B) d += "&" + a.B;
                var g = a.t,
                    m = g[r],
                    y = [],
                    N = [];
                for (var s in g) if (s != V) if (s.indexOf("_") != 0) {
                    var O = g[s][1];
                    if (O) g[O] && N[k](s + "." + X(a, s, g[O][0]));
                    else m && y[k](s + "." + X(a, s))
                }
                delete g[r];
                if (b) for (var U in b) d += "&" + U + "=" + b[U];
                return a = [c ? c : "//www.google.com/csi", "?v=3", "&s=" + (h.gpjstiming.sn || "mog") + "&action=", a.name, N[l] ? "&it=" + N.join(",") : J, J, d, "&rt=", y.join(",")].join(J)
            };
        h.gpjstiming.report = function (a, b, c) {
            a = ba(a, b, c);
            b = new Image;
            var d = h.gpjstiming.H++;
            h.gpjstiming.m[d] = b;
            b.onload = b.onerror = function () {
                delete h.gpjstiming.m[d]
            };
            b.src = a;
            b = e;
            return a
        }
    };

    function Y() {
        this.A = this.n = this.s = this.d = e
    }
    Y[n].I = function (a) {
        this.d = a
    };
    Y[n].sci = Y[n].I;

    function Z(a, b, c) {
        this.h = a;
        this.raw = this.f = b;
        this.env = this.b = c;
        this.k = this.l = true
    }
    Z[n].start = function (a) {
        var b = new this.f.Timer;
        j(b, a);
        b.c = this.b.d;
        b.a = e;
        this.v();
        return b
    };
    Z[n].start = Z[n][r];
    Z[n].loaded = function (a) {
        a[q](V);
        a[q]("ol");
        var b = this.o();
        a.a = b.a;
        a.c = b.c
    };
    Z[n].loaded = Z[n].loaded;
    var $ = "prt";
    Z[n].F = function (a) {
        a[q]($);
        this[u](a)
    };
    Z[n].done = Z[n].F;
    Z[n].report = function (a, b, c) {
        b = b || {};
        b.e = this.b.s;
        b.mog_d = this.b.n ? "1" : "0";
        b.mog_ui = this.b.A;
        var d = a.c,
            g = a.C,
            m = d && g,
            y = m && d != g;
        if (y) {
            b.mog_transition = d + ":" + g;
            this.b.d = g
        }
        if (!m || y) if (a.a !== e) b.srt = a.a;
        this.f[u](a, b, c)
    };
    Z[n].report = Z[n][u];
    Z[n].D = function () {
        this.k = this.l = f
    };
    Z[n].datr = Z[n].D;
    Z[n].w = function () {
        this.f.load[q]($)
    };
    Z[n].tdt = Z[n].w;
    Z[n].u = function () {
        this[u](this.f.load)
    };
    Z[n].rdt = Z[n].u;
    var ca = /^smog@bnt@(\d+)@o@([^@]+)@emog$/;
    Z[n].v = function () {
        j(this.h, "smog@bnt@" + this.r() + "@o@" + this.b.d + "@emog")
    };
    Z[n].o = function () {
        var a = {};
        a.a = e;
        a.c = e;
        var b = ca.exec(this.h.name);
        if (b) {
            j(this.h, J);
            var c = Number(b[1]);
            if (!isFinite(c)) return a;
            var d = this.r() - c;
            if (d > 6E5) return a;
            this.bnt = c;
            a.a = d;
            a.c = b[2]
        }
        return a
    };
    Z[n].r = function () {
        return (new Date).getTime()
    };
    Z[n].G = function () {
        D && this.j(D.getElementsByTagName(I));
        A && this.j(A.getElementsByTagName(I))
    };
    Z[n].i = Z[n].G;
    Z[n].j = function (a) {
        for (var b = this, c = function () {
            b.v()
        }, d = 0, g = a[l]; d < g; d++) a[d][t](R, c, f)
    };

    function da(a, b) {
        a[q]("ol");
        b.l && b.w();
        b.k && x.setTimeout(function () {
            b.u()
        }, 1E3)
    }
    function ea() {
        var a = new Y;
        a.d = "1";
        a.s = "0";
        a.n = "";
        a.A = "4";
        var b = x.gpjstiming.load;
        j(b, "default_load_1");
        var c = new Z(x, x.gpjstiming, a);
        x.og.csi = c;
        var d = c.o();
        b.a = d.a;
        b.c = d.c;
        b.C = a.d;
        x[t]("load", function () {
            da(b, c)
        }, f)
    }
    ea();

    function fa() {
        ga(z);
        for (var a = parseInt(F(z, "font-size"), 10), b = M(), c = i[o]("og_s").sheet, d = f, g = function () {
            var m = D[p];
            if (B) m += B[p];
            if (E) m += E[p];
            m += 7;
            return m
        }; g() > b;) {
            d && c.deleteRule(c.cssRules[l] - 1);
            d = true;
            c.insertRule("#og_head,#og_head div{font-size:" + a + "px !important;}", c.cssRules[l]);
            a--;
            if (a <= 8) break
        }
    }
    function ga(a) {
        for (var b = a.childNodes, c = b[l] - 1; c >= 0; c--) b[c].nodeType == 3 && a.removeChild(b[c])
    }
    w[k](fa);
    var ha = "//ssl.gstatic.com/m/og/s14" + "_en.js".toLowerCase().replace("-", "_");

    function ia() {
        var a = i.createElement("script");
        a.src = ha;
        i.body.appendChild(a)
    }
    h.og.z = ia;
    w[k](function () {
        E[t](R, function () {
            h.og.z()
        }, f)
    });
})(); /* ]]> */
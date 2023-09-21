# 2022-07-15: rascunho criado a partir de código antigo

def cwt_calc_peaks(valid_xpks, valid_ypks, valid_cwtpks, xs, y0s):
    # Calcular centroide com base em corte linear da linha base
    # fazer a busca em duas passadas.

    n_side_chans = 11
    n_side_centr_ch = 5
    # constante k: ver no Maxima: (sqrt(3)*6^(3/2))/(2^(3/2)*5^(5/4)*%pi^(1/4));
    k = (np.sqrt(3) * 6 ** (3 / 2)) / (2 ** (3 / 2) * 5 ** (5 / 4) * np.pi ** (1 / 4))
    kfwhm = 2 * np.sqrt(2 * np.log(2))
    karea = np.sqrt(2 * np.pi)

    regions_slcs = []
    centrpk = []
    azes = []
    bezes = []
    ypkregs = []
    fwhms = []
    gau_areas = []
    unc_gau_areas = []
    peak_constructed_spectrum = np.zeros(len(xs))

    for ipk, pk in enumerate(valid_xpks):
        escalmaxima = valid_ypks[ipk]
        maxcwt = valid_cwtpks[ipk]
        # centroide = centrpk[ipk]
        sigmamaximo = escalmaxima / np.sqrt(5)
        fwhm = kfwhm * sigmamaximo
        gau_hei = k * maxcwt / np.sqrt(sigmamaximo)
        gau_area = gau_hei * sigmamaximo * karea
        # 2020-02-22 Vari'avel n~ao usada:
        # region_start = regions_slcs[ipk].start
        # 2019-10-02 C'alculo de centroide
        # 2020-02-23 Constr'oi linha base linear na regi~ao de c'alculo da centroide
        bline_for_centr = np.linspace(y0s[pk - n_side_centr_ch],
                                      y0s[pk + n_side_centr_ch],
                                      num=2 * n_side_centr_ch + 1)
        region_centr = slice(pk - n_side_centr_ch, pk + n_side_centr_ch + 1)
        nety_for_centr = y0s[region_centr] - bline_for_centr

        a = xs[region_centr]
        b = nety_for_centr
        azes.append(a)
        bezes.append(b)
        centrpk.append(np.sum(a * b) / np.sum(b))

        # subtrair o pica v'alido
        region_slc = slice(pk - n_side_chans, pk + n_side_chans + 1)
        regions_slcs.append(region_slc)
        ypicoregio = gaus_sig(xs[region_slc], sigmamaximo, gau_hei, centrpk[-1])
        ypkregs.append(ypicoregio)
        fwhms.append(fwhm)
        gau_areas.append(gau_area)
        peak_constructed_spectrum[region_slc] += ypicoregio

    baseline_spectrum = y0s - peak_constructed_spectrum
    len_bl = len(baseline_spectrum)
    bl_median_smoother = np.zeros(len_bl)
    bl_median_smoother[20:len_bl - 20] = np.asarray(
        [np.median(baseline_spectrum[i - n_side_chans:i + n_side_chans + 1]) for i in range(20, len_bl - 20)])
    ret = (azes, bezes, centrpk, ypkregs, fwhms, gau_areas, peak_constructed_spectrum,
           baseline_spectrum, bl_median_smoother)
    return ret


def cwt_complete_analysis(counts):
    """
    Return the results from cwt analysis on a num sequence.

    Parameters
    ----------
    counts
        A num sequence containing the spetrum counts per channel.

    """

    # pk_per_scal - list of arrays, where each one is the positions of peaks
    # found by find_peaks_cwt on each scale in widths

    spLngData = len(counts)

    # 2020-02-21 Arbitrary...
    # 2020-04-25 Coloquei 0.003 (era 0.002) para picos larguissimos de I-131
    upper_scale = spLngData * 0.003
    widths = np.linspace(2, upper_scale, num=50)
    min_cwtpk = 30.0
    nsca_det = 5

    # min_snr = 1.0
    # noise_perc = 3.0
    min_snr = 1.0
    noise_perc = 10.0

    xs = np.linspace(0, spLngData - 1, spLngData)
    y0s = np.asarray(counts)

    pk_per_scal = []
    for wid in widths:
        pk_per_scal.append(find_peaks_cwt(
            y0s, widths=[wid], wavelet=ricker,
            min_snr=min_snr, noise_perc=noise_perc))
    #

    pks_cwt_flatten = []
    for isc, pksc in enumerate(pk_per_scal):
        for pk in pksc:
            pks_cwt_flatten.append([pk, widths[isc]])
    ar1 = np.asarray(pks_cwt_flatten)

    # imag1: imagem de pixels binahrios dos picos nas escalas
    imag1 = np.zeros((len(widths), len(xs)))
    for isc, pksc in enumerate(pk_per_scal):
        for pk in pksc:
            imag1[isc, pk] = 1
    # 2020-02-23  Comandos-chave para identificar os ridges por imagem:
    stru_diag_also = generate_binary_structure(2, 2)
    lblimag1, num_feat_imag1 = label(imag1, stru_diag_also)
    ridges = find_objects(lblimag1)
    cwtmatr = cwt(y0s, ricker, widths)

    xpks = []
    ypks = []
    ind_ypks = []
    retang_indicess = []
    cwtpks = []
    nscpks = []
    valid_position_in_ridges = []
    for iridge, ridge in enumerate(ridges):
        lbl_ridge = iridge + 1
        nscpk_ini = ridge[0].start
        nscpk_fin = ridge[0].stop
        nscpks.append(nscpk_fin - nscpk_ini)
        labeled = lblimag1[ridge]
        cwts_ridge = cwtmatr[ridge]
        retang3 = ma.masked_where(labeled != lbl_ridge, cwts_ridge)
        maxim3 = np.max(retang3)
        flat_retang_ind = np.argmax(retang3)
        retang_indices = np.unravel_index(flat_retang_ind, np.shape(retang3))
        indices_max_in_ridge = tuple(map(lambda x, y: x + y, retang_indices, (ridge[0].start, ridge[1].start)))
        cwtpks.append(maxim3)
        xpk = indices_max_in_ridge[1]
        ind_ypk = indices_max_in_ridge[0]
        valid_position_in_ridges.append(ind_ypk in range(nscpk_ini + 2, nscpk_fin - 2))
        ypk = widths[ind_ypk]
        xpks.append(xpk)
        ypks.append(ypk)
        ind_ypks.append(ind_ypk)
        retang_indicess.append(retang_indices)
    # 2020-02-23
    # Crit'erios para picos v'alidos:
    # Picos n~ao pr'oximos dos extremos dos espectros
    # pico com cwt m'aximo na escala entre 3 e 13 (espectro 8k)
    # essa escala n~ao pode estar nas extremidades do ridge
    # cwt m'aximo: 30 ?
    # no gr'afico de ridges distinguir picos por cor

    xpks = np.asarray(xpks)
    ypks = np.asarray(ypks)
    # o pico deve aparecer em pelo menos nsca_det (default 5) escalas
    nscpk_ma = ma.masked_less(nscpks, nsca_det)
    # o coeficiente cwt deve ser >= min_cwtpk (default 30.0)
    cwtpk_ma = ma.masked_less(cwtpks, min_cwtpk)
    # o cwt m'aximo n~ao pode estar pr'oximo aos extremos do ridge
    pospk_ma = ma.masked_where(False, valid_position_in_ridges)
    # 2020-02-21
    # widpk_ma = ma.masked_less(cwtpk, min_cwtpk)

    peaks_masks = (nscpk_ma, cwtpk_ma, pospk_ma)

    ret = (xs, y0s, ar1, lblimag1, num_feat_imag1, ridges, xpks, ypks,
           ind_ypks, retang_indicess, peaks_masks,
           cwtpks, nscpks)
    return ret


def gaussian_complete_analysis(counts):
    """
    Return the results from cwt analysis on a num sequence.

    Parameters
    ----------
    counts
        A num sequence containing the spetrum counts per channel.

    """

    # pk_per_scal - list of arrays, where each one is the positions of peaks
    # found by find_peaks_cwt on each scale in widths

    spLngData = len(counts)

    # 2020-02-21 Arbitrary...
    # 2020-04-25 Coloquei 0.003 (era 0.002) para picos larguissimos de I-131
    upper_scale = spLngData * 0.003
    widths = np.linspace(2, upper_scale, num=50)
    min_cwtpk = 30.0
    nsca_det = 5

    # min_snr = 1.0
    # noise_perc = 3.0
    min_snr = 1.0
    noise_perc = 10.0

    n_side_chans = 11
    n_side_centr_ch = 5
    # constante k: ver no Maxima: (sqrt(3)*6^(3/2))/(2^(3/2)*5^(5/4)*%pi^(1/4));
    k = (np.sqrt(3) * 6 ** (3 / 2)) / (2 ** (3 / 2) * 5 ** (5 / 4) * np.pi ** (1 / 4))
    kfwhm = 2 * np.sqrt(2 * np.log(2))
    karea = np.sqrt(2 * np.pi)

    xs = np.linspace(0, spLngData - 1, spLngData)
    y0s = np.asarray(counts)

    len_bl = len(y0s)
    baseline_spectrum = np.zeros(len_bl)
    baseline_spectrum[20:len_bl - 20] = np.asarray(
        [np.amin(y0s[i - n_side_chans:i + n_side_chans + 1]) for i in range(20, len_bl - 20)])

    # 2020-04-25 PAREI AQUIIIIIIIIII

    # baseline_spectrum = y0s - peak_constructed_spectrum
    # len_bl = len(baseline_spectrum)
    # bl_median_smoother = np.zeros(len_bl)
    # bl_median_smoother[20:len_bl-20] = np.asarray(
    #         [np.median(baseline_spectrum[i-n_side_chans:i+n_side_chans+1]) for i in range(20,len_bl-20) ])
    # ret = (azes, bezes, centrpk, ypkregs, fwhms, gau_areas, peak_constructed_spectrum,
    #        baseline_spectrum, bl_median_smoother )

    pk_per_scal = []
    for wid in widths:
        pk_per_scal.append(find_peaks_cwt(
            y0s, widths=[wid], wavelet=ricker,
            min_snr=min_snr, noise_perc=noise_perc))
    #

    pks_cwt_flatten = []
    for isc, pksc in enumerate(pk_per_scal):
        for pk in pksc:
            pks_cwt_flatten.append([pk, widths[isc]])
    ar1 = np.asarray(pks_cwt_flatten)

    # imag1: imagem de pixels binahrios dos picos nas escalas
    imag1 = np.zeros((len(widths), len(xs)))
    for isc, pksc in enumerate(pk_per_scal):
        for pk in pksc:
            imag1[isc, pk] = 1
    # 2020-02-23  Comandos-chave para identificar os ridges por imagem:
    stru_diag_also = generate_binary_structure(2, 2)
    lblimag1, num_feat_imag1 = label(imag1, stru_diag_also)
    ridges = find_objects(lblimag1)
    cwtmatr = cwt(y0s, ricker, widths)

    xpks = []
    ypks = []
    ind_ypks = []
    retang_indicess = []
    cwtpks = []
    nscpks = []
    valid_position_in_ridges = []
    for iridge, ridge in enumerate(ridges):
        lbl_ridge = iridge + 1
        nscpk_ini = ridge[0].start
        nscpk_fin = ridge[0].stop
        nscpks.append(nscpk_fin - nscpk_ini)
        labeled = lblimag1[ridge]
        cwts_ridge = cwtmatr[ridge]
        retang3 = ma.masked_where(labeled != lbl_ridge, cwts_ridge)
        maxim3 = np.max(retang3)
        flat_retang_ind = np.argmax(retang3)
        retang_indices = np.unravel_index(flat_retang_ind, np.shape(retang3))
        indices_max_in_ridge = tuple(map(lambda x, y: x + y, retang_indices, (ridge[0].start, ridge[1].start)))
        cwtpks.append(maxim3)
        xpk = indices_max_in_ridge[1]
        ind_ypk = indices_max_in_ridge[0]
        valid_position_in_ridges.append(ind_ypk in range(nscpk_ini + 2, nscpk_fin - 2))
        ypk = widths[ind_ypk]
        xpks.append(xpk)
        ypks.append(ypk)
        ind_ypks.append(ind_ypk)
        retang_indicess.append(retang_indices)
    # 2020-02-23
    # Crit'erios para picos v'alidos:
    # Picos n~ao pr'oximos dos extremos dos espectros
    # pico com cwt m'aximo na escala entre 3 e 13 (espectro 8k)
    # essa escala n~ao pode estar nas extremidades do ridge
    # cwt m'aximo: 30 ?
    # no gr'afico de ridges distinguir picos por cor

    xpks = np.asarray(xpks)
    ypks = np.asarray(ypks)
    # o pico deve aparecer em pelo menos nsca_det (default 5) escalas
    nscpk_ma = ma.masked_less(nscpks, nsca_det)
    # o coeficiente cwt deve ser >= min_cwtpk (default 30.0)
    cwtpk_ma = ma.masked_less(cwtpks, min_cwtpk)
    # o cwt m'aximo n~ao pode estar pr'oximo aos extremos do ridge
    pospk_ma = ma.masked_where(False, valid_position_in_ridges)
    # 2020-02-21
    # widpk_ma = ma.masked_less(cwtpk, min_cwtpk)

    peaks_masks = (nscpk_ma, cwtpk_ma, pospk_ma)

    ret = (xs, y0s, ar1, lblimag1, num_feat_imag1, ridges, xpks, ypks,
           ind_ypks, retang_indicess, peaks_masks,
           cwtpks, nscpks)
    return ret

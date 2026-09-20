# -*- coding: utf-8 -*-
"""
Script to generate the complete, enhanced Dashboard Dept SMTI HTML file
with:
1. Manual checklist input & task deletion
2. User comments / team notes feed with timestamps and avatars
3. Flexible stage status & manual progress controls (handle completed, active, pending, reopen)
4. LocalStorage persistence for user inputs and notes
"""

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Dept SMTI - PT Pupuk Kujang</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary-color: #1e3a8a;
            --primary-dark: #0f172a;
            --secondary-color: #0284c7;
            --accent-color: #ef4444;
            --bg-color: #f1f5f9;
            --text-color: #1e293b;
            --white: #ffffff;
            --hover-color: #e2e8f0;
            --card-bg: #ffffff;
            --border-color: #cbd5e1;
            
            /* Urgency Colors */
            --urgency-high: #dc2626;
            --urgency-high-bg: rgba(220, 38, 38, 0.12);
            --urgency-med: #d97706;
            --urgency-med-bg: rgba(217, 119, 6, 0.12);
            --urgency-low: #16a34a;
            --urgency-low-bg: rgba(22, 163, 74, 0.12);
        }

        body.dark-mode {
            --primary-color: #1e293b;
            --primary-dark: #0b0f19;
            --secondary-color: #38bdf8;
            --accent-color: #f87171;
            --bg-color: #0f172a;
            --text-color: #f1f5f9;
            --white: #1e293b;
            --card-bg: #1e293b;
            --hover-color: #334155;
            --border-color: #334155;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-color); display: flex; min-height: 100vh; transition: background-color 0.3s, color 0.3s; }

        /* --- SIDEBAR --- */
        .sidebar { width: 260px; background-color: #0f172a; color: #ffffff; display: flex; flex-direction: column; padding: 20px; position: fixed; height: 100%; z-index: 100; justify-content: space-between; border-right: 1px solid rgba(255,255,255,0.08); }
        .sidebar-top { flex: 1; overflow-y: auto; }
        .sidebar-brand { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.12); }
        .sidebar-brand-icon { width: 42px; height: 42px; background: linear-gradient(135deg, #0284c7, #10b981); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: white; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3); }
        .sidebar-brand-text h2 { font-size: 16px; font-weight: 700; color: #fff; letter-spacing: 0.5px; line-height: 1.2; }
        .sidebar-brand-text small { font-size: 11px; color: #94a3b8; letter-spacing: 0.3px; }
        
        .menu-category { font-size: 11px; text-transform: uppercase; color: #64748b; margin: 16px 0 6px 8px; font-weight: 700; letter-spacing: 0.8px; }
        .menu-item { padding: 11px 14px; cursor: pointer; transition: 0.2s; border-radius: 8px; margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between; color: #94a3b8; font-size: 13.5px; font-weight: 500; }
        .menu-item-left { display: flex; align-items: center; gap: 12px; }
        .menu-item:hover { background-color: rgba(255,255,255,0.08); color: white; }
        .menu-item.active { background-color: #0284c7; color: white; font-weight: 600; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25); }
        .menu-item i { width: 20px; font-size: 15px; text-align: center; }
        .menu-badge { background: rgba(255,255,255,0.18); font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: 600; }
        .menu-badge.badge-urgent { background: #dc2626; color: white; animation: pulseRed 2s infinite; }
        .menu-badge.badge-live { background: #10b981; color: white; font-weight: 700; letter-spacing: 0.5px; }

        /* FOOTER SIDEBAR */
        .sidebar-footer { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px; margin-top: 15px; }
        .user-card { display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-bottom: 10px; }
        .user-avatar { width: 36px; height: 36px; background: linear-gradient(135deg, #0284c7, #0ea5e9); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; }
        .user-info { flex: 1; overflow: hidden; }
        .user-info .name { font-size: 13px; font-weight: 600; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .user-info .role { font-size: 11px; color: #94a3b8; }
        
        .logout-btn { width: 100%; padding: 9px; background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 6px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 12.5px; font-weight: 600; transition: 0.2s; }
        .logout-btn:hover { background: #ef4444; color: white; }

        /* --- MAIN CONTENT --- */
        .main-content { margin-left: 260px; flex: 1; padding: 20px; width: calc(100% - 260px); }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; background: var(--white); padding: 14px 22px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.04); position: relative; gap: 15px; flex-wrap: wrap; border: 1px solid var(--border-color); }

        .header-left { display: flex; align-items: center; gap: 15px; }
        .header-title h1 { font-size: 20px; font-weight: 700; color: var(--text-color); }
        .header-title small { font-size: 12px; color: #64748b; font-weight: 500; }
        
        .status-badge { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #16a34a; background: rgba(22, 163, 74, 0.1); padding: 5px 12px; border-radius: 20px; font-weight: 600; }
        .status-dot { width: 8px; height: 8px; background-color: #16a34a; border-radius: 50%; display: inline-block; animation: pulseGreen 1.8s infinite; }
        @keyframes pulseGreen { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.2); } 100% { opacity: 1; transform: scale(1); } }
        @keyframes pulseRed { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.1); } 100% { opacity: 1; transform: scale(1); } }

        .time-display { font-size: 13px; font-weight: 600; color: var(--text-color); background: var(--hover-color); padding: 6px 12px; border-radius: 6px; }

        .cloud-sync-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 700;
            background: rgba(16, 185, 129, 0.12);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }

        .cloud-sync-badge:hover {
            background: rgba(16, 185, 129, 0.22);
            transform: translateY(-1px);
        }

        .cloud-sync-badge.syncing {
            background: rgba(245, 158, 11, 0.12);
            color: #f59e0b;
            border-color: rgba(245, 158, 11, 0.35);
        }

        .cloud-sync-badge.error {
            background: rgba(239, 68, 68, 0.12);
            color: #ef4444;
            border-color: rgba(239, 68, 68, 0.35);
        }

        .header-actions { display: flex; align-items: center; gap: 12px; }
        
        /* Tombol Mode Monitor TV di Header */
        .btn-monitor-mode { background: linear-gradient(135deg, #dc2626, #ea580c); color: white; border: none; padding: 8px 15px; border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 12px rgba(220, 38, 38, 0.25); transition: 0.2s; animation: pulseRed 2.5s infinite; }
        .btn-monitor-mode:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(220, 38, 38, 0.35); }

        .global-search { position: relative; width: 220px; }
        .global-search input { width: 100%; padding: 8px 12px 8px 34px; border: 1px solid var(--border-color); border-radius: 20px; outline: none; background: var(--bg-color); color: var(--text-color); font-size: 13px; }
        .global-search i { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #888; font-size: 12px; }

        .quick-add-btn { background: #16a34a; color: white; border: none; border-radius: 50%; width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; }
        .quick-add-btn:hover { background: #15803d; transform: scale(1.05); }

        .icon-btn { position: relative; cursor: pointer; font-size: 18px; color: var(--text-color); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; background: var(--hover-color); transition: 0.2s; }
        .icon-btn:hover { color: var(--secondary-color); }
        .icon-btn .badge { position: absolute; top: -4px; right: -4px; background: var(--accent-color); color: white; font-size: 10px; border-radius: 10px; padding: 2px 6px; font-weight: 700; }

        .dropdown-menu { display: none; position: absolute; top: 60px; right: 20px; background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); width: 270px; z-index: 150; padding: 10px; }
        .dropdown-menu.active { display: block; animation: fadeIn 0.2s ease; }
        .dropdown-item { padding: 9px 12px; font-size: 13px; border-bottom: 1px solid var(--border-color); display: flex; align-items: center; gap: 10px; cursor: pointer; border-radius: 6px; }
        .dropdown-item:hover { background: var(--hover-color); }
        .dropdown-item:last-child { border-bottom: none; }

        /* --- SECTION LOGIC --- */
        .page-section { display: none; animation: fadeIn 0.2s ease; }
        .page-section.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

        /* Cards & Grids */
        .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px; }
        .card { background: var(--card-bg); padding: 20px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.04); margin-bottom: 20px; border: 1px solid var(--border-color); }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; font-weight: 700; font-size: 16px; }
        .chart-container { position: relative; height: 320px; width: 100%; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 12px 14px; border-bottom: 1px solid var(--border-color); text-align: left; font-size: 13px; }
        tbody tr:hover { background-color: var(--hover-color); cursor: pointer; }
        
        .status { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
        .btn { padding: 8px 16px; font-size: 13px; background: var(--secondary-color); color: white; border: none; border-radius: 6px; cursor: pointer; transition: 0.2s; display: inline-flex; align-items: center; gap: 6px; font-weight: 600; }
        .btn:hover { background: #0369a1; }
        .btn-sm { padding: 5px 10px; font-size: 12px; }

        /* Profile Detail View */
        #detail-karyawan { display: none; }
        .profile-view { text-align: center; padding: 20px; }
        .avatar-big { width: 90px; height: 90px; background: var(--secondary-color); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 36px; margin: 0 auto 15px; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.2); }

        /* Filter, Modals, Notifikasi */
        .filter-container { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
        .filter-input, .filter-select { padding: 8px 12px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 13px; outline: none; background: var(--card-bg); color: var(--text-color); }
        .filter-input { flex: 1; min-width: 200px; }
        .action-btn { padding: 5px 9px; border: none; border-radius: 5px; cursor: pointer; font-size: 12px; margin-left: 4px; }
        .btn-edit { background: #d97706; color: white; }
        .btn-delete { background: #dc2626; color: white; }

        /* Modal System - Smooth Scroll & Fit Viewport */
        .modal {
            display: none;
            position: fixed;
            z-index: 100000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(15, 23, 42, 0.72);
            backdrop-filter: blur(6px);
            align-items: center;
            justify-content: center;
            overflow-y: auto;
            padding: 20px 10px;
            box-sizing: border-box;
        }
        .modal-content {
            background-color: var(--card-bg);
            color: var(--text-color);
            padding: 24px;
            border-radius: 14px;
            width: 480px;
            max-width: 95%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 50px rgba(0,0,0,0.35);
            border: 1px solid var(--border-color);
            margin: auto;
            position: relative;
        }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
        .close-modal { cursor: pointer; font-size: 20px; color: #888; }
        .form-group { margin-bottom: 14px; }
        .form-group label { display: block; font-size: 12px; font-weight: 600; opacity: 0.8; margin-bottom: 5px; }
        .form-group input:not([type="checkbox"]):not([type="radio"]), .form-group select, .form-group textarea { width: 100%; padding: 9px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 13px; background: var(--card-bg); color: var(--text-color); outline: none; }
        input[type="checkbox"], input[type="radio"] { width: auto !important; min-width: 16px; height: 16px; cursor: pointer; flex-shrink: 0; }

        /* PIN Authentication Overlay */
        .pin-auth-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            width: 100vw; height: 100vh;
            background: radial-gradient(circle at 50% 20%, rgba(2, 132, 199, 0.25) 0%, rgba(15, 23, 42, 0.96) 75%);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            z-index: 999999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            box-sizing: border-box;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }
        .pin-auth-overlay.hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
        .pin-auth-card {
            background: var(--card-bg, #ffffff);
            border: 1px solid var(--border-color, #e2e8f0);
            border-radius: 16px;
            width: 440px;
            max-width: 96%;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.45);
            overflow: hidden;
            animation: pinSlideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes pinSlideUp {
            from { opacity: 0; transform: translateY(24px) scale(0.96); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .pin-auth-header {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: white;
            padding: 26px 24px 20px;
            text-align: center;
            position: relative;
        }
        .pin-auth-logo {
            width: 52px;
            height: 52px;
            background: rgba(255, 255, 255, 0.2);
            border: 2px solid rgba(255, 255, 255, 0.4);
            border-radius: 50%;
            margin: 0 auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            color: #ffffff;
            box-shadow: 0 6px 14px rgba(0,0,0,0.15);
        }
        .pin-auth-header h2 {
            font-size: 15.5px;
            font-weight: 800;
            margin: 0;
            letter-spacing: 0.2px;
        }
        .pin-auth-header p {
            font-size: 12px;
            margin: 4px 0 0;
            opacity: 0.9;
        }
        .pin-auth-body {
            padding: 22px 24px;
        }
        .pin-form-group {
            margin-bottom: 16px;
        }
        .pin-form-group label {
            display: block;
            font-size: 12px;
            font-weight: 700;
            color: var(--text-color, #1e293b);
            margin-bottom: 6px;
        }
        .pin-user-select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--border-color, #cbd5e1);
            border-radius: 8px;
            background: var(--card-bg, #ffffff);
            color: var(--text-color, #1e293b);
            font-size: 13px;
            font-weight: 600;
            outline: none;
            cursor: pointer;
        }
        .pin-user-preview {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            background: var(--hover-color, #f8fafc);
            border: 1px solid var(--border-color, #e2e8f0);
            border-radius: 10px;
            margin-bottom: 16px;
        }
        .pin-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            color: white;
            font-weight: 800;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .pin-user-meta {
            flex: 1;
            min-width: 0;
        }
        .pin-user-meta strong {
            display: block;
            font-size: 13.5px;
            color: var(--text-color, #1e293b);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .pin-user-meta div {
            font-size: 11px;
            color: #64748b;
            margin-top: 1px;
        }
        .pin-role-badge {
            font-size: 10px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 12px;
            white-space: nowrap;
        }
        .pin-input-container {
            position: relative;
            display: flex;
            align-items: center;
        }
        .pin-input-field {
            width: 100%;
            padding: 12px 42px 12px 16px;
            border: 2px solid var(--border-color, #cbd5e1);
            border-radius: 8px;
            font-size: 20px;
            font-weight: 700;
            text-align: center;
            letter-spacing: 6px;
            background: var(--bg-color, #ffffff);
            color: var(--text-color, #1e293b);
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .pin-input-field:focus {
            border-color: #0284c7;
            box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.2);
        }
        .pin-input-field.shake {
            animation: pinShake 0.4s ease-in-out;
            border-color: #dc2626 !important;
        }
        @keyframes pinShake {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-8px); }
            40%, 80% { transform: translateX(8px); }
        }
        .pin-toggle-btn {
            position: absolute;
            right: 12px;
            background: transparent;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            font-size: 15px;
            padding: 4px;
        }
        .pin-error-msg {
            color: #dc2626;
            font-size: 11.5px;
            font-weight: 600;
            margin-top: 6px;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .pin-remember-box {
            margin-bottom: 18px;
        }
        .pin-remember-box label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            color: var(--text-color, #475569);
            cursor: pointer;
        }
        .btn-submit-pin {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
            transition: 0.2s ease;
        }
        .btn-submit-pin:hover {
            filter: brightness(1.08);
            transform: translateY(-1px);
        }
        .pin-help-accordion {
            margin-top: 14px;
            text-align: center;
        }
        .pin-help-toggle {
            background: transparent;
            border: none;
            color: #0284c7;
            font-size: 11.5px;
            font-weight: 600;
            cursor: pointer;
            padding: 4px;
        }

        /* Settings & FAQ */
        .setting-group { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid var(--border-color); }
        .setting-group:last-child { border-bottom: none; }
        .faq-item { margin-bottom: 15px; border-bottom: 1px solid var(--border-color); padding-bottom: 12px; }
        .faq-title { font-weight: 600; cursor: pointer; color: var(--secondary-color); margin-bottom: 6px; font-size: 14px; }

        /* =========================================================
           FITUR PROYEK & URGENSI
           ========================================================= */
        .project-kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin-bottom: 18px; }
        .project-kpi-card { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 15px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.03); }
        .project-kpi-info small { font-size: 11px; text-transform: uppercase; font-weight: 700; opacity: 0.7; }
        .project-kpi-info h3 { font-size: 24px; font-weight: 800; margin-top: 3px; }
        .project-kpi-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
        
        .kpi-total { border-left: 4px solid #0284c7; }
        .kpi-total .project-kpi-icon { background: rgba(2, 132, 199, 0.12); color: #0284c7; }
        
        .kpi-high { border-left: 4px solid #dc2626; }
        .kpi-high .project-kpi-icon { background: rgba(220, 38, 38, 0.12); color: #dc2626; }
        
        .kpi-med { border-left: 4px solid #d97706; }
        .kpi-med .project-kpi-icon { background: rgba(217, 119, 6, 0.12); color: #d97706; }
        
        .kpi-low { border-left: 4px solid #16a34a; }
        .kpi-low .project-kpi-icon { background: rgba(22, 163, 74, 0.12); color: #16a34a; }

        /* Filter Controls */
        .project-toolbar { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
        .project-tabs { display: flex; gap: 6px; flex-wrap: wrap; }
        .tab-btn { padding: 7px 14px; border: 1px solid var(--border-color); background: var(--bg-color); color: var(--text-color); border-radius: 6px; cursor: pointer; font-size: 12.5px; font-weight: 600; transition: 0.2s; display: flex; align-items: center; gap: 6px; }
        .tab-btn:hover { background: var(--hover-color); }
        .tab-btn.active { background: var(--secondary-color); color: white; border-color: var(--secondary-color); }
        .tab-btn.tab-urgent.active { background: #dc2626; border-color: #dc2626; }

        /* Project Cards List */
        .project-card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; }
        .project-card-item { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 18px; box-shadow: 0 2px 6px rgba(0,0,0,0.03); transition: transform 0.2s, box-shadow 0.2s; position: relative; display: flex; flex-direction: column; justify-content: space-between; }
        .project-card-item:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
        
        .card-urgency-high { border-top: 4px solid #dc2626; }
        .card-urgency-med { border-top: 4px solid #d97706; }
        .card-urgency-low { border-top: 4px solid #16a34a; }
        .card-status-completed { border-top: 4px solid #16a34a !important; }
        .tab-btn.tab-completed { border-color: #16a34a; color: #16a34a; }
        .tab-btn.tab-completed:hover { background: rgba(22, 163, 74, 0.1); }
        .tab-btn.tab-completed.active { background: #16a34a !important; border-color: #16a34a !important; color: #ffffff !important; }
        .tab-btn.tab-completed.active i { color: #ffffff !important; }
        .tab-btn.tab-running { border-color: #0284c7; color: #0284c7; }
        .tab-btn.tab-running:hover { background: rgba(2, 132, 199, 0.1); }
        .tab-btn.tab-running.active { background: #0284c7 !important; border-color: #0284c7 !important; color: #ffffff !important; }

        .project-card-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; margin-bottom: 10px; }
        .project-category-tag { font-size: 10px; font-weight: 700; text-transform: uppercase; color: #64748b; background: var(--hover-color); padding: 3px 8px; border-radius: 4px; }
        
        .urgency-badge { font-size: 10.5px; font-weight: 700; padding: 4px 10px; border-radius: 20px; display: inline-flex; align-items: center; gap: 5px; }
        .urgency-badge.high { background: rgba(220, 38, 38, 0.12); color: #dc2626; border: 1px solid rgba(220, 38, 38, 0.25); }
        .urgency-badge.med { background: rgba(217, 119, 6, 0.12); color: #d97706; border: 1px solid rgba(217, 119, 6, 0.25); }
        .urgency-badge.low { background: rgba(22, 163, 74, 0.12); color: #16a34a; border: 1px solid rgba(22, 163, 74, 0.25); }

        .project-card-title { font-size: 15px; font-weight: 700; margin-bottom: 6px; line-height: 1.35; }
        .project-card-desc { font-size: 12px; color: #64748b; line-height: 1.5; margin-bottom: 12px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }

        /* Flow Stepper Mini Preview on Card */
        .card-flow-preview { background: var(--hover-color); padding: 10px 12px; border-radius: 8px; margin-bottom: 14px; }
        .card-flow-header { display: flex; justify-content: space-between; align-items: center; font-size: 11px; margin-bottom: 6px; font-weight: 600; }
        .mini-stepper { display: flex; align-items: center; justify-content: space-between; position: relative; }
        .mini-step-node { width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; z-index: 2; border: 2px solid var(--card-bg); }
        .mini-step-node.completed { background: #16a34a; color: white; }
        .mini-step-node.active { background: #0284c7; color: white; box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.25); animation: pulseGreen 1.5s infinite; }
        .mini-step-node.pending { background: #cbd5e1; color: #475569; }
        .mini-stepper-line { position: absolute; left: 10px; right: 10px; height: 2px; background: #cbd5e1; z-index: 1; }

        .project-card-meta { display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: #64748b; margin-bottom: 14px; border-top: 1px solid var(--border-color); padding-top: 10px; }
        .project-deadline-pill { background: rgba(220, 38, 38, 0.1); color: #dc2626; padding: 2px 7px; border-radius: 4px; font-weight: 700; font-size: 11px; }

        .btn-view-flow { width: 100%; padding: 9px; background: linear-gradient(135deg, var(--secondary-color), #0369a1); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 12.5px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; transition: 0.2s; }
        .btn-view-flow:hover { background: #0284c7; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3); }

        /* =========================================================
           MODE MONITOR TV / REMINDER DISPLAY (FULLSCREEN KIOSK)
           ========================================================= */
        #monitor-overlay {
            display: none;
            position: fixed;
            inset: 0;
            z-index: 99999;
            background: #090d16;
            color: #f8fafc;
            overflow-y: auto;
            flex-direction: column;
            padding: 20px 30px;
        }

        #monitor-overlay.active {
            display: flex;
        }

        .monitor-topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255,255,255,0.12);
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 15px;
        }

        .monitor-brand {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .monitor-brand-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #dc2626, #ef4444);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
            box-shadow: 0 0 20px rgba(220, 38, 38, 0.5);
            animation: pulseRed 2s infinite;
        }

        .monitor-brand-text h1 {
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .monitor-live-tag {
            font-size: 11px;
            background: #10b981;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            animation: pulseGreen 1.5s infinite;
        }

        .monitor-brand-text p {
            font-size: 12px;
            color: #94a3b8;
        }

        .monitor-clock-box {
            text-align: center;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 8px 24px;
            border-radius: 12px;
        }

        .monitor-clock-time {
            font-size: 28px;
            font-weight: 800;
            color: #38bdf8;
            font-family: 'Consolas', monospace;
            letter-spacing: 1px;
        }

        .monitor-clock-date {
            font-size: 12px;
            color: #cbd5e1;
        }

        .monitor-controls {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .monitor-btn {
            background: rgba(255,255,255,0.1);
            color: white;
            border: 1px solid rgba(255,255,255,0.18);
            padding: 9px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: 0.2s;
        }

        .monitor-btn:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-1px);
        }

        .monitor-btn.btn-close-monitor {
            background: rgba(220, 38, 38, 0.2);
            border-color: rgba(220, 38, 38, 0.4);
            color: #fca5a5;
        }

        .monitor-btn.btn-close-monitor:hover {
            background: #dc2626;
            color: white;
        }

        /* Running Ticker Marquee Pengingat */
        .monitor-ticker-wrap {
            background: rgba(220, 38, 38, 0.15);
            border: 1px solid rgba(220, 38, 38, 0.35);
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            height: 42px;
        }

        .ticker-label {
            background: #dc2626;
            color: white;
            font-weight: 800;
            font-size: 12px;
            padding: 0 16px;
            height: 100%;
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
            letter-spacing: 0.5px;
            z-index: 2;
        }

        .ticker-marquee {
            flex: 1;
            overflow: hidden;
            white-space: nowrap;
            padding-left: 20px;
        }

        .ticker-track {
            display: inline-block;
            white-space: nowrap;
            animation: marquee 35s linear infinite;
            font-size: 13px;
            color: #fecaca;
            font-weight: 600;
        }

        @keyframes marquee {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }

        /* Monitor Filter Bar */
        .monitor-filter-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.035);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 12px;
            padding: 10px 18px;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 14px;
        }

        .monitor-filter-left {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }

        .monitor-filter-right {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .monitor-filter-title {
            font-size: 11.5px;
            font-weight: 800;
            color: #94a3b8;
            letter-spacing: 0.8px;
            display: flex;
            align-items: center;
            gap: 6px;
            text-transform: uppercase;
        }

        .monitor-filter-pills {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            align-items: center;
        }

        .mon-pill-btn {
            background: rgba(255, 255, 255, 0.06);
            color: #cbd5e1;
            border: 1px solid rgba(255, 255, 255, 0.12);
            padding: 7px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
        }

        .mon-pill-btn:hover {
            background: rgba(255, 255, 255, 0.14);
            color: #ffffff;
            transform: translateY(-1px);
        }

        .mon-pill-btn .mon-pill-count {
            background: rgba(255, 255, 255, 0.15);
            padding: 1px 7px;
            border-radius: 10px;
            font-size: 10.5px;
            font-weight: 800;
        }

        .mon-pill-btn.active {
            background: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 0 16px rgba(2, 132, 199, 0.45);
        }

        .mon-pill-btn.mon-pill-high.active {
            background: #dc2626;
            color: #ffffff;
            border-color: #f87171;
            box-shadow: 0 0 18px rgba(220, 38, 38, 0.5);
        }

        .mon-pill-btn.mon-pill-high:hover:not(.active) {
            border-color: rgba(220, 38, 38, 0.5);
            color: #fca5a5;
        }

        .mon-pill-btn.mon-pill-med.active {
            background: #d97706;
            color: #ffffff;
            border-color: #fbbf24;
            box-shadow: 0 0 18px rgba(217, 119, 6, 0.5);
        }

        .mon-pill-btn.mon-pill-med:hover:not(.active) {
            border-color: rgba(217, 119, 6, 0.4);
            color: #fde68a;
        }

        .mon-pill-btn.mon-pill-low.active {
            background: #16a34a;
            color: #ffffff;
            border-color: #4ade80;
            box-shadow: 0 0 18px rgba(22, 163, 74, 0.5);
        }

        .mon-pill-btn.mon-pill-low:hover:not(.active) {
            border-color: rgba(22, 163, 74, 0.4);
            color: #86efac;
        }

        .mon-cat-select {
            background: rgba(15, 23, 42, 0.85);
            color: #f8fafc;
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 8px;
            padding: 7px 12px;
            font-size: 12px;
            font-weight: 600;
            outline: none;
            cursor: pointer;
            transition: 0.2s;
        }

        .mon-cat-select:hover, .mon-cat-select:focus {
            border-color: #38bdf8;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.25);
        }

        /* Monitor Urgency Board */
        .monitor-board {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            flex: 1;
            transition: all 0.3s ease;
        }

        .monitor-card-list.monitor-card-list-expanded {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 16px;
        }

        .monitor-column {
            background: rgba(255,255,255,0.03);
            border-radius: 14px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            border: 1px solid rgba(255,255,255,0.08);
        }

        .monitor-col-high { border-top: 4px solid #dc2626; background: rgba(220, 38, 38, 0.04); }
        .monitor-col-med { border-top: 4px solid #d97706; background: rgba(217, 119, 6, 0.04); }
        .monitor-col-low { border-top: 4px solid #16a34a; background: rgba(22, 163, 74, 0.04); }

        .monitor-col-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 12px;
            margin-bottom: 14px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }

        .monitor-col-header h3 {
            font-size: 15px;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: 0.5px;
        }

        .monitor-col-high .monitor-col-header h3 { color: #f87171; }
        .monitor-col-med .monitor-col-header h3 { color: #fbbf24; }
        .monitor-col-low .monitor-col-header h3 { color: #4ade80; }

        .monitor-col-badge {
            background: rgba(255,255,255,0.1);
            font-size: 11px;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 700;
        }

        .monitor-card-list {
            display: flex;
            flex-direction: column;
            gap: 14px;
            flex: 1;
        }

        .monitor-project-card {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 12px;
            padding: 16px;
            cursor: pointer;
            transition: 0.25s;
            position: relative;
        }

        .monitor-project-card:hover {
            background: rgba(30, 41, 59, 1);
            border-color: #38bdf8;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }

        .monitor-card-high {
            border-left: 4px solid #dc2626;
            box-shadow: 0 0 15px rgba(220, 38, 38, 0.1);
        }

        .monitor-card-med {
            border-left: 4px solid #d97706;
        }

        .monitor-card-low {
            border-left: 4px solid #16a34a;
        }

        .monitor-card-title {
            font-size: 14px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
            line-height: 1.35;
        }

        .monitor-card-stage {
            font-size: 11.5px;
            color: #94a3b8;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .monitor-stage-highlight {
            color: #38bdf8;
            font-weight: 600;
        }

        .monitor-progress-box {
            margin-bottom: 12px;
        }

        .monitor-progress-label {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #cbd5e1;
            margin-bottom: 4px;
            font-weight: 600;
        }

        .monitor-progress-track {
            height: 7px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
        }

        .monitor-progress-bar {
            height: 100%;
            border-radius: 10px;
            transition: width 0.4s ease;
        }

        .bar-high { background: linear-gradient(90deg, #dc2626, #f87171); }
        .bar-med { background: linear-gradient(90deg, #d97706, #fbbf24); }
        .bar-low { background: linear-gradient(90deg, #16a34a, #4ade80); }

        .monitor-card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: #94a3b8;
            border-top: 1px solid rgba(255,255,255,0.08);
            padding-top: 8px;
        }

        .monitor-click-hint {
            color: #38bdf8;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* =========================================================
           MODAL FLOW PROGRES INTERAKTIF (ENHANCED)
           ========================================================= */
        #flowModal {
            display: none;
            position: fixed;
            inset: 0;
            z-index: 100000;
            background: rgba(15, 23, 42, 0.78);
            backdrop-filter: blur(8px);
            align-items: center;
            justify-content: center;
            padding: 15px;
        }

        #flowModal.active {
            display: flex;
        }

        .flow-modal-box {
            width: 900px;
            max-width: 96%;
            max-height: 92vh;
            overflow-y: auto;
            background: var(--card-bg);
            color: var(--text-color);
            border-radius: 16px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.38);
            border: 1px solid var(--border-color);
            animation: modalPopIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        @keyframes modalPopIn {
            from { opacity: 0; transform: scale(0.92) translateY(20px); }
            to { opacity: 1; transform: scale(1) translateY(0); }
        }

        .flow-modal-header {
            padding: 20px 26px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 15px;
            background: var(--hover-color);
            border-radius: 16px 16px 0 0;
        }

        .flow-modal-header h2 {
            font-size: 19px;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .flow-modal-close {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 16px;
            color: var(--text-color);
            transition: 0.2s;
        }

        .flow-modal-close:hover {
            background: #ef4444;
            color: white;
            border-color: #ef4444;
        }

        .flow-modal-body {
            padding: 22px 26px;
        }

        /* Status & Progress Quick Control Toolbar */
        .stage-control-toolbar {
            background: var(--hover-color);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        .stage-status-actions {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        .stage-status-btn {
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            border: 1px solid var(--border-color);
            background: var(--card-bg);
            color: var(--text-color);
            cursor: pointer;
            transition: 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }

        .stage-status-btn:hover {
            transform: translateY(-1px);
        }

        .stage-status-btn.btn-set-completed { background: #16a34a; color: white; border-color: #16a34a; }
        .stage-status-btn.btn-set-active { background: #0284c7; color: white; border-color: #0284c7; }
        .stage-status-btn.btn-set-pending { background: #64748b; color: white; border-color: #64748b; }

        .progress-manual-box {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 600;
        }

        .progress-manual-input {
            width: 60px;
            padding: 5px 8px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-weight: 700;
            text-align: center;
            background: var(--card-bg);
            color: var(--text-color);
        }

        /* Project Highlights Grid in Modal */
        .flow-meta-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }

        .flow-meta-item {
            background: var(--hover-color);
            padding: 12px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }

        .flow-meta-item small {
            font-size: 10px;
            text-transform: uppercase;
            font-weight: 700;
            opacity: 0.65;
            display: block;
            margin-bottom: 3px;
        }

        .flow-meta-item strong {
            font-size: 13.5px;
        }

        /* Stepper Flow Interactive Diagram */
        .flow-stepper-container {
            margin-bottom: 20px;
            background: var(--hover-color);
            padding: 18px 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }

        .flow-stepper-title {
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stepper-pipeline {
            display: flex;
            justify-content: space-between;
            position: relative;
            margin-bottom: 10px;
        }

        .stepper-pipeline::before {
            content: '';
            position: absolute;
            top: 20px;
            left: 25px;
            right: 25px;
            height: 4px;
            background: var(--border-color);
            z-index: 1;
        }

        .step-item {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            flex: 1;
            padding: 0 6px;
            transition: 0.2s;
        }

        .step-item:hover .step-circle {
            transform: scale(1.15);
        }

        .step-circle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--card-bg);
            border: 3px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 14px;
            margin-bottom: 8px;
            transition: 0.25s;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }

        .step-item.completed .step-circle {
            background: #16a34a;
            border-color: #16a34a;
            color: white;
        }

        .step-item.active .step-circle {
            background: #0284c7;
            border-color: #0284c7;
            color: white;
            box-shadow: 0 0 0 5px rgba(2, 132, 199, 0.25);
            animation: pulseGreen 1.6s infinite;
        }

        .step-item.pending .step-circle {
            background: var(--card-bg);
            border-color: var(--border-color);
            color: #94a3b8;
        }

        .step-name {
            font-size: 11px;
            font-weight: 700;
            text-align: center;
            line-height: 1.3;
            max-width: 120px;
        }

        .step-date {
            font-size: 10px;
            color: #64748b;
            margin-top: 3px;
        }

        /* Detail Step Card */
        .active-stage-detail {
            background: var(--card-bg);
            border: 2px solid var(--secondary-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.04);
        }

        .stage-detail-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border-color);
        }

        .stage-badge-current {
            background: #0284c7;
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 12px;
        }

        .stage-badge-urgent {
            background: #dc2626;
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 12px;
            animation: pulseRed 2s infinite;
        }

        /* Tasks Checklist */
        .task-checklist {
            margin-top: 16px;
        }

        .task-checklist-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .task-checklist h4 {
            font-size: 13.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .task-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 9px 12px;
            background: var(--hover-color);
            border-radius: 6px;
            margin-bottom: 6px;
            font-size: 13px;
            cursor: pointer;
            transition: 0.2s;
            border: 1px solid transparent;
        }

        .task-item:hover {
            border-color: var(--border-color);
        }

        .task-left {
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
        }

        .task-item input[type="checkbox"] {
            width: 17px;
            height: 17px;
            cursor: pointer;
        }

        .task-item.checked span {
            text-decoration: line-through;
            opacity: 0.6;
        }

        .task-delete-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            cursor: pointer;
            font-size: 12px;
            padding: 4px 6px;
            border-radius: 4px;
            transition: 0.2s;
        }

        .task-delete-btn:hover {
            color: #ef4444;
            background: rgba(239, 68, 68, 0.1);
        }

        /* Form Input Tambah Tugas Manual */
        .add-task-form {
            display: flex;
            gap: 8px;
            margin-top: 12px;
        }

        .add-task-input {
            flex: 1;
            padding: 8px 12px;
            border: 1px dashed var(--border-color);
            border-radius: 6px;
            font-size: 12.5px;
            background: var(--card-bg);
            color: var(--text-color);
            outline: none;
        }

        .add-task-input:focus {
            border-style: solid;
            border-color: var(--secondary-color);
        }

        .stage-alert-box {
            background: rgba(220, 38, 38, 0.1);
            border-left: 4px solid #dc2626;
            padding: 12px 14px;
            border-radius: 6px;
            font-size: 12.5px;
            color: #dc2626;
            font-weight: 600;
            margin-top: 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
        }

        /* =========================================================
           KOMENTAR & CATATAN PENGGUNA / TIM (DISCUSSION FEED)
           ========================================================= */
        /* Tim Proyek & Member Invite */
        .project-team-section {
            background: var(--hover-color);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px 18px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        .team-bar-left {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .team-bar-label {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-color);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .team-avatars-list {
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
        }

        .team-member-pill {
            display: flex;
            align-items: center;
            gap: 6px;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 3px 10px 3px 4px;
            font-size: 11.5px;
            font-weight: 600;
            color: var(--text-color);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .team-avatar-circle {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            color: white;
            font-size: 10px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .team-member-remove {
            background: transparent;
            border: none;
            color: #ef4444;
            cursor: pointer;
            font-size: 11px;
            padding: 2px 4px;
            margin-left: 2px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .team-member-remove:hover {
            background: rgba(239, 68, 68, 0.15);
        }

        .btn-invite-team {
            background: linear-gradient(135deg, #0284c7, #0369a1);
            color: white;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: 0.2s;
        }
        .btn-invite-team:hover {
            background: #0284c7;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
        }

        /* Progress Chat Tags */
        .progress-chat-tag {
            font-size: 10.5px;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .tag-progress { background: rgba(2, 132, 199, 0.12); color: #0284c7; border: 1px solid rgba(2, 132, 199, 0.3); }
        .tag-done { background: rgba(22, 163, 74, 0.12); color: #16a34a; border: 1px solid rgba(22, 163, 74, 0.3); }
        .tag-issue { background: rgba(220, 38, 38, 0.12); color: #dc2626; border: 1px solid rgba(220, 38, 38, 0.3); }
        .tag-note { background: rgba(217, 119, 6, 0.12); color: #d97706; border: 1px solid rgba(217, 119, 6, 0.3); }

        .comments-section {
            background: var(--hover-color);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 20px;
        }

        .comments-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }

        .comments-header h4 {
            font-size: 13.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .comments-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 220px;
            overflow-y: auto;
            margin-bottom: 14px;
            padding-right: 5px;
        }

        .comment-item {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 12.5px;
        }

        .comment-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
        }

        .comment-author-badge {
            font-weight: 700;
            color: var(--secondary-color);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .comment-time {
            font-size: 10.5px;
            color: #64748b;
        }

        .comment-text {
            color: var(--text-color);
            line-height: 1.4;
        }

        .comment-form {
            display: flex;
            gap: 8px;
        }

        .comment-input {
            flex: 1;
            padding: 9px 12px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 12.5px;
            background: var(--card-bg);
            color: var(--text-color);
            outline: none;
        }

        .comment-input:focus {
            border-color: var(--secondary-color);
        }

        .flow-modal-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            border-top: 1px solid var(--border-color);
            padding-top: 18px;
            margin-top: 20px;
        }

        @media (max-width: 900px) {
            .monitor-board { grid-template-columns: 1fr; }
            .flow-meta-grid { grid-template-columns: repeat(2, 1fr); }
            .stepper-pipeline { flex-direction: column; gap: 15px; }
            .stepper-pipeline::before { display: none; }
            .step-item { flex-direction: row; gap: 12px; }
            .step-name { text-align: left; }
        }
    </style>
</head>
<body>

    <!-- =========================================================
         OVERLAY LOGIN PIN PENGGUNA SMTI (AUTO-REMEMBER BROWSER)
         ========================================================= -->
    <div id="pin-auth-overlay" class="pin-auth-overlay">
        <div class="pin-auth-card">
            <div class="pin-auth-header">
                <div class="pin-auth-logo">
                    <i class="fas fa-shield-alt"></i>
                </div>
                <h2>Sistem Manajemen Terpadu & Inovasi</h2>
                <p>PT Pupuk Kujang Cikampek • Departemen SMTI</p>
            </div>

            <div class="pin-auth-body">
                <div class="pin-form-group">
                    <label><i class="fas fa-user-circle"></i> Pilih Profil Pengguna Anda:</label>
                    <select id="pin-user-select" class="pin-user-select" onchange="onPinUserSelected(this.value)">
                        <!-- Populated dynamically via JS -->
                    </select>
                </div>

                <div id="pin-user-preview" class="pin-user-preview">
                    <div class="pin-avatar" id="pin-preview-avatar">S</div>
                    <div class="pin-user-meta">
                        <strong id="pin-preview-name">Septian</strong>
                        <div id="pin-preview-role">Super Admin & Officer Digitalisasi</div>
                    </div>
                    <span id="pin-preview-badge" class="pin-role-badge">Super Admin</span>
                </div>

                <div class="pin-form-group">
                    <label><i class="fas fa-key"></i> Masukkan PIN Keamanan (4 Digit):</label>
                    <div class="pin-input-container">
                        <input type="password" id="pin-input-code" maxlength="6" class="pin-input-field" placeholder="••••" autocomplete="off" inputmode="numeric" onkeydown="handlePinKeyDown(event)">
                        <button type="button" class="pin-toggle-btn" onclick="togglePinVisibility()" title="Lihat / Sembunyikan PIN">
                            <i class="fas fa-eye" id="pin-eye-icon"></i>
                        </button>
                    </div>
                    <div id="pin-error-msg" class="pin-error-msg" style="display: none;"></div>
                </div>

                <div class="pin-remember-box">
                    <label>
                        <input type="checkbox" id="pin-remember-device" checked>
                        <span><strong>Ingat di browser ini</strong> (Otomatis masuk tanpa ketik PIN lagi)</span>
                    </label>
                </div>

                <button type="button" class="btn-submit-pin" onclick="verifyAndLoginPin()">
                    <i class="fas fa-unlock-alt"></i> Buka Dashboard SMTI
                </button>

                <div class="pin-help-accordion">
                    <button type="button" class="pin-help-toggle" onclick="togglePinHelp()">
                        <i class="fas fa-info-circle"></i> Bantuan & Daftar PIN Awal Pengguna
                    </button>
                    <div id="pin-help-content" style="display: none; text-align: left; margin-top: 8px; font-size: 11.5px; background: var(--hover-color); padding: 10px 12px; border-radius: 8px; border: 1px solid var(--border-color); color: var(--text-color);">
                        <p style="margin: 0 0 6px 0; font-weight: 700; color: #0284c7;">
                            <i class="fas fa-user-lock"></i> PIN Awal Default: <code>1234</code>
                        </p>
                        <ul style="margin: 0; padding-left: 18px; line-height: 1.5;">
                            <li><strong>Septian:</strong> Super Admin (PIN: <code>1234</code>)</li>
                            <li><strong>Henisya Permata Sari:</strong> Manager Dept SMTI (PIN: <code>1234</code>)</li>
                            <li><strong>Karyawan Lainnya:</strong> PIN: <code>1234</code></li>
                        </ul>
                        <p style="margin: 6px 0 0 0; font-size: 11px; color: #16a34a; font-weight: 600;">
                            ✓ Centang <em>"Ingat di browser ini"</em> agar login otomatis dan tidak perlu isi PIN lagi di kunjungan berikutnya!
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- SIDEBAR -->
    <div class="sidebar">
        <div class="sidebar-top">
            <div class="sidebar-brand">
                <div class="sidebar-brand-icon">
                    <i class="fas fa-cubes"></i>
                </div>
                <div class="sidebar-brand-text">
                    <h2>DEPT. SMTI</h2>
                    <small>PT PUPUK KUJANG</small>
                </div>
            </div>
            
            <div class="menu-category">Menu Utama</div>
            <div class="menu-item active" onclick="showPage('dasbor', this)">
                <div class="menu-item-left"><i class="fas fa-chart-line"></i> <span>Dasbor</span></div>
            </div>
            <div class="menu-item" onclick="showPage('proyek', this)">
                <div class="menu-item-left"><i class="fas fa-project-diagram"></i> <span>Proyek Berjalan</span></div>
                <span class="menu-badge badge-urgent" id="side-urgent-count">3 Urgent</span>
            </div>
            <div class="menu-item" onclick="openMonitorMode()">
                <div class="menu-item-left"><i class="fas fa-desktop"></i> <span>Layar Monitor</span></div>
                <span class="menu-badge badge-live">LIVE</span>
            </div>
            <div class="menu-item" id="menu-item-karyawan" onclick="showPage('karyawan', this)">
                <div class="menu-item-left"><i class="fas fa-users"></i> <span>Karyawan SMTI</span></div>
                <span class="menu-badge" id="side-karyawan-count">10</span>
            </div>
            <div class="menu-item" id="menu-item-magang" onclick="showPage('magang', this)">
                <div class="menu-item-left"><i class="fas fa-user-graduate"></i> <span>Anak Magang / PKL</span></div>
                <span class="menu-badge" id="side-magang-count" style="background: rgba(16, 185, 129, 0.25); color: #10b981; font-weight: 700;">4</span>
            </div>

            <div class="menu-category" id="menu-cat-system">Sistem & Laporan</div>
            <div class="menu-item" onclick="showPage('laporan', this)">
                <div class="menu-item-left"><i class="fas fa-file-alt"></i> <span>Laporan Analytics</span></div>
            </div>
            <div class="menu-item" id="menu-item-pengaturan" onclick="showPage('pengaturan', this)">
                <div class="menu-item-left"><i class="fas fa-cog"></i> <span>Pengaturan</span></div>
            </div>
            <div class="menu-item" id="menu-item-bantuan" onclick="showPage('bantuan', this)">
                <div class="menu-item-left"><i class="fas fa-question-circle"></i> <span>Bantuan</span></div>
            </div>
        </div>

        <!-- FOOTER SIDEBAR -->
        <div class="sidebar-footer">
            <div class="user-card">
                <div class="user-avatar">A</div>
                <div class="user-info">
                    <div class="name">Administrator SMTI</div>
                    <div class="role">admin@pupuk-kujang.co.id</div>
                </div>
            </div>
            <button class="logout-btn" onclick="handleLogout()">
                <i class="fas fa-sign-out-alt"></i> Keluar Akun
            </button>
        </div>
    </div>

    <!-- MAIN CONTENT -->
    <div class="main-content">
        <div class="header">
            <div class="header-left">
                <div class="header-title">
                    <h1 id="current-title">Ringkasan Performa SMTI</h1>
                    <small>Sistem Manajemen Terpadu & Inovasi • PT Pupuk Kujang</small>
                </div>
                
                <div class="status-badge">
                    <span class="status-dot"></span> System Live
                </div>
            </div>
            
            <div class="header-actions">
                <button class="btn-monitor-mode" onclick="openMonitorMode()" title="Buka Mode Layar Monitor / TV Pengingat">
                    <i class="fas fa-desktop"></i> Mode Monitor TV
                </button>

                <div class="global-search">
                    <i class="fas fa-search"></i>
                    <input type="text" placeholder="Cari proyek / karyawan..." onkeyup="handleGlobalSearch(event)">
                </div>

                <div class="cloud-sync-badge" id="cloud-sync-badge" onclick="syncFromCloud(true)" title="Data tersimpan di Vercel Cloud Storage. Klik untuk menyegarkan data.">
                    <i class="fas fa-cloud"></i> <span id="cloud-sync-text">Vercel Terhubung</span>
                </div>

                <div class="time-display" id="live-clock">--:--:-- WIB</div>

                <div class="icon-btn" onclick="toggleDarkMode()" title="Ubah Mode Gelap/Terang">
                    <i class="fas fa-moon" id="theme-icon"></i>
                </div>

                <div class="icon-btn" onclick="toggleDropdown('notif-dropdown')" title="Notifikasi">
                    <i class="fas fa-bell"></i>
                    <span class="badge" id="notif-badge-count">3</span>
                </div>

                <div style="display: flex; align-items: center; gap: 9px; cursor: pointer; padding: 4px 8px; border-radius: 8px; background: var(--hover-color); border: 1px solid var(--border-color);" onclick="toggleDropdown('profile-dropdown')" title="Profil Pengguna & Pengaturan Akun">
                    <div class="user-avatar" id="top-user-avatar" style="width: 32px; height: 32px; font-size: 11.5px; font-weight: 700; background: #06b6d4;">SP</div>
                    <div style="text-align: right; line-height: 1.25;" class="desktop-only">
                        <div id="top-user-name" style="font-size: 12px; font-weight: 700; color: var(--text-color);">Septian</div>
                        <div id="top-user-role" style="font-size: 10px; font-weight: 700; color: #0891b2;"><i class="fas fa-shield-alt"></i> Super Admin</div>
                    </div>
                    <i class="fas fa-chevron-down" style="font-size: 10px; color: #94a3b8; margin-left: 2px;"></i>
                </div>
            </div>

            <!-- Notif Dropdown -->
            <div id="notif-dropdown" class="dropdown-menu">
                <div style="font-weight: 700; margin-bottom: 8px; font-size: 13px; color: var(--text-color);">Pengingat Proyek & Sistem</div>
                <div class="dropdown-item" onclick="openFlowModal(1)">
                    <i class="fas fa-exclamation-triangle" style="color: #dc2626;"></i>
                    <div>
                        <strong>KIX Prototyping (Urgensi Tinggi)</strong>
                        <div style="font-size: 11px; opacity: 0.7;">72.8% peserta belum mengisi form</div>
                    </div>
                </div>
                <div class="dropdown-item" onclick="openFlowModal(3)">
                    <i class="fas fa-shield-alt" style="color: #dc2626;"></i>
                    <div>
                        <strong>Audit Eksternal ISO 27001</strong>
                        <div style="font-size: 11px; opacity: 0.7;">Roadshow tindak lanjut audit berjalan</div>
                    </div>
                </div>
                <div class="dropdown-item" onclick="openFlowModal(4)">
                    <i class="fas fa-award" style="color: #d97706;"></i>
                    <div>
                        <strong>ICCOSH Yogyakarta</strong>
                        <div style="font-size: 11px; opacity: 0.7;">Menunggu kelengkapan dokumen 3 gugus</div>
                    </div>
                </div>
            </div>

            <!-- Profile Dropdown -->
            <div id="profile-dropdown" class="dropdown-menu" style="min-width: 240px;">
                <div style="padding: 10px 12px; margin-bottom: 5px; border-bottom: 1px solid var(--border-color); background: var(--hover-color); border-radius: 8px 8px 0 0;">
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 3px;">
                        <strong id="drop-user-name" style="font-size: 13.5px; color: var(--text-color);">Septian</strong>
                        <span id="drop-user-badge" style="font-size: 9.5px; font-weight: 700; padding: 2px 7px; border-radius: 10px; background: rgba(6, 182, 212, 0.15); color: #0891b2; border: 1px solid #67e8f9;">Super Admin</span>
                    </div>
                    <div id="drop-user-role" style="font-size: 11px; color: #64748b;">Super Admin & Officer Digitalisasi</div>
                </div>
                <div class="dropdown-item" onclick="openChangePinModal()"><i class="fas fa-key" style="color: #f59e0b;"></i> Ganti PIN Keamanan</div>
                <div class="dropdown-item" id="drop-item-pengaturan" onclick="showPage('pengaturan', null)"><i class="fas fa-user-cog" style="color: #0284c7;"></i> Pengaturan Akun</div>
                <div class="dropdown-item" onclick="openMonitorMode()"><i class="fas fa-tv" style="color: #10b981;"></i> Buka Tampilan Monitor</div>
                <div class="dropdown-item" style="color: #dc2626; font-weight: 700; border-top: 1px solid var(--border-color); margin-top: 4px; padding-top: 8px;" onclick="handleLogout()"><i class="fas fa-sign-out-alt"></i> Kunci Layar / Ganti Akun</div>
            </div>
        </div>

        <!-- ================= PAGE DASBOR ================= -->
        <div id="dasbor" class="page-section active">
            <div class="dashboard-grid">
                <div class="card" style="border-left: 4px solid #0284c7;">
                    <div class="card-header"><span>Total Proyek Berjalan</span><i class="fas fa-tasks" style="color: #0284c7;"></i></div>
                    <h2 id="dash-total-proyek" style="font-size: 30px; font-weight: 800;">8</h2>
                    <small style="color: #64748b;">Inovasi, Mutu, & Digitalisasi</small>
                </div>
                <div class="card" style="border-left: 4px solid #dc2626;">
                    <div class="card-header"><span>Proyek Urgensi Tinggi</span><i class="fas fa-bell" style="color: #dc2626;"></i></div>
                    <h2 id="dash-urgent-proyek" style="font-size: 30px; font-weight: 800; color: #dc2626;">3</h2>
                    <small style="color: #dc2626; font-weight: 600;"><i class="fas fa-clock"></i> Membutuhkan Tindakan Segera</small>
                </div>
                <div class="card" style="border-left: 4px solid #d97706;">
                    <div class="card-header"><span>Urgensi Sedang</span><i class="fas fa-hourglass-half" style="color: #d97706;"></i></div>
                    <h2 id="dash-med-proyek" style="font-size: 30px; font-weight: 800; color: #d97706;">3</h2>
                    <small style="color: #64748b;">Dalam Pengawalan Rutin</small>
                </div>
                <div class="card" style="border-left: 4px solid #16a34a;">
                    <div class="card-header"><span>Total Karyawan</span><i class="fas fa-users" style="color: #16a34a;"></i></div>
                    <h2 id="dash-karyawan-count" style="font-size: 30px; font-weight: 800;">10</h2>
                    <small style="color: #64748b;">Tim SMTI & PMSMT</small>
                </div>
            </div>

            <!-- Urgent Highlight Banner on Dashboard -->
            <div class="card" style="background: linear-gradient(135deg, rgba(220, 38, 38, 0.06), rgba(2, 132, 199, 0.06)); border: 1px solid rgba(220, 38, 38, 0.2);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span class="urgency-badge high" style="margin-bottom: 6px;"><i class="fas fa-exclamation-circle"></i> PENGINGAT DEADLINE SEGERA</span>
                        <h3 style="font-size: 17px; font-weight: 700;">KIX - Prototyping and Pitch Preparation</h3>
                        <p style="font-size: 13px; color: #64748b; margin-top: 4px;">Pendampingan intensif peserta internal & afiliasi PT Pupuk Kujang. Target Pitching: 15 Mei 2026.</p>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button class="btn" style="background: #dc2626;" onclick="openFlowModal(1)"><i class="fas fa-sitemap"></i> Buka Alur & Input Checklist</button>
                        <button class="btn" onclick="openMonitorMode()"><i class="fas fa-desktop"></i> Pantau di Monitor</button>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <span>Tren Produktivitas & Kinerja Mingguan SMTI</span>
                    <small style="font-weight: normal; color: #64748b;">Realisasi Kegiatan Q2-Q3 2026</small>
                </div>
                <div class="chart-container">
                    <canvas id="mainChart"></canvas>
                </div>
            </div>
        </div>

        <!-- ================= PAGE PROYEK BERJALAN ================= -->
        <div id="proyek" class="page-section">
            <!-- Project KPIs -->
            <div class="project-kpi-grid">
                <div class="project-kpi-card kpi-total" onclick="filterProjects('semua', document.querySelector('.tab-btn[data-filter=\'semua\']'))" style="cursor: pointer;" title="Klik untuk menampilkan semua proyek">
                    <div class="project-kpi-info">
                        <small>Total Proyek</small>
                        <h3 id="proyek-kpi-total">10</h3>
                    </div>
                    <div class="project-kpi-icon"><i class="fas fa-folder-open"></i></div>
                </div>
                <div class="project-kpi-card" onclick="filterProjects('running', document.querySelector('.tab-btn[data-filter=\'running\']'))" style="border-left: 4px solid #0284c7; cursor: pointer;" title="Klik untuk memfilter proyek sedang berjalan">
                    <div class="project-kpi-info">
                        <small>Sedang Berjalan</small>
                        <h3 id="proyek-kpi-running" style="color: #0284c7;">8</h3>
                    </div>
                    <div class="project-kpi-icon" style="background: rgba(2, 132, 199, 0.12); color: #0284c7;"><i class="fas fa-spinner"></i></div>
                </div>
                <div class="project-kpi-card kpi-completed" onclick="filterProjects('selesai', document.querySelector('.tab-btn[data-filter=\'selesai\']'))" style="border-left: 4px solid #16a34a; cursor: pointer;" title="Klik untuk memfilter proyek yang sudah selesai">
                    <div class="project-kpi-info">
                        <small>Sudah Selesai</small>
                        <h3 id="proyek-kpi-completed" style="color: #16a34a;">2</h3>
                    </div>
                    <div class="project-kpi-icon" style="background: rgba(22, 163, 74, 0.12); color: #16a34a;"><i class="fas fa-check-double"></i></div>
                </div>
                <div class="project-kpi-card kpi-high" onclick="filterProjects('Tinggi', document.querySelector('.tab-btn[data-filter=\'Tinggi\']'))" style="cursor: pointer;" title="Klik untuk memfilter proyek urgensi tinggi">
                    <div class="project-kpi-info">
                        <small>Urgensi Tinggi</small>
                        <h3 id="proyek-kpi-high" style="color: #dc2626;">3</h3>
                    </div>
                    <div class="project-kpi-icon"><i class="fas fa-fire"></i></div>
                </div>
            </div>

            <!-- Toolbar & Filter -->
            <div class="project-toolbar">
                <div class="project-tabs">
                    <button class="tab-btn active" data-filter="semua" onclick="filterProjects('semua', this)">
                        <i class="fas fa-layer-group"></i> Semua (<span id="count-proj-all">0</span>)
                    </button>
                    <button class="tab-btn tab-running" data-filter="running" onclick="filterProjects('running', this)">
                        <i class="fas fa-spinner"></i> Sedang Berjalan (<span id="count-proj-running">0</span>)
                    </button>
                    <button class="tab-btn tab-completed" data-filter="selesai" onclick="filterProjects('selesai', this)">
                        <i class="fas fa-check-circle" style="color: #16a34a;"></i> Sudah Selesai (<span id="count-proj-completed">0</span>)
                    </button>
                    <button class="tab-btn tab-urgent" data-filter="Tinggi" onclick="filterProjects('Tinggi', this)">
                        <i class="fas fa-fire"></i> Urgensi Tinggi (<span id="count-proj-high">0</span>)
                    </button>
                    <button class="tab-btn" data-filter="Sedang" onclick="filterProjects('Sedang', this)">
                        <i class="fas fa-clock"></i> Urgensi Sedang (<span id="count-proj-med">0</span>)
                    </button>
                    <button class="tab-btn" data-filter="Rendah" onclick="filterProjects('Rendah', this)">
                        <i class="fas fa-tasks"></i> Rutin / Rendah (<span id="count-proj-low">0</span>)
                    </button>
                </div>

                <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                    <select id="category-filter-select" onchange="filterByCategory(this.value)" class="filter-select" style="font-weight: 600; padding: 7px 10px; min-width: 170px;">
                        <option value="semua">Semua Kategori (3 Bidang)</option>
                        <option value="MIKU">MIKU</option>
                        <option value="PMSMT">PMSMT</option>
                        <option value="Pengembangan Sistem dan Prosedur">Pengembangan Sistem & Prosedur</option>
                    </select>
                    <div class="global-search" style="width: 180px;">
                        <i class="fas fa-search"></i>
                        <input type="text" id="project-search-box" placeholder="Cari proyek..." onkeyup="searchProjects(event)">
                    </div>
                    <button class="btn" style="background: #0284c7;" onclick="openAddProjectModal()">
                        <i class="fas fa-plus-circle"></i> Tambah Proyek Baru
                    </button>
                    <button class="btn btn-sm" style="background: #64748b;" onclick="resetToDefaultData()" title="Reset data simulasi ke awal">
                        <i class="fas fa-redo"></i> Reset
                    </button>
                    <button class="btn" style="background: #16a34a;" onclick="openMonitorMode()">
                        <i class="fas fa-tv"></i> Mode Layar Monitor
                    </button>
                </div>
            </div>

            <!-- Project Cards Grid -->
            <div class="project-card-grid" id="project-card-container">
                <!-- Dynamically Rendered by JavaScript -->
            </div>
        </div>

        <!-- ================= PAGE KARYAWAN ================= -->
        <div id="karyawan" class="page-section">
            <div id="list-karyawan">
                <div class="card">
                    <div class="card-header">
                        <span>Daftar Karyawan Dept SMTI</span>
                        <div style="display: flex; gap: 8px;">
                            <button class="btn" style="background: #16a34a;" onclick="exportTableToCSV()"><i class="fas fa-file-excel"></i> Export CSV</button>
                            <button class="btn super-admin-only" id="btn-tambah-karyawan" onclick="openModal()"><i class="fas fa-plus"></i> Tambah Karyawan</button>
                        </div>
                    </div>

                    <div class="filter-container">
                        <input type="text" id="search-input" class="filter-input" placeholder="Cari nama atau jabatan..." onkeyup="filterKaryawan()">
                        <select id="status-filter" class="filter-select" onchange="filterKaryawan()">
                            <option value="">Semua Status</option>
                            <option value="TKO">TKO (Operasional)</option>
                            <option value="TKNO">TKNO (Non-Operasional)</option>
                        </select>
                    </div>

                    <table>
                        <thead>
                            <tr><th>Nama Karyawan</th><th>Jabatan</th><th>Status</th><th>Aksi</th></tr>
                        </thead>
                        <tbody id="employee-table-body">
                            <tr onclick="viewDetail('Henisya Permata Sari', 'VP SMTI', 'TKO', '#d4edda')">
                                <td><strong>Henisya Permata Sari</strong></td><td>VP SMTI</td><td><span class="status" style="background: #d4edda; color: #155724;">TKO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Mochamad Januardi', 'Officer Inovasi', 'TKO', '#d4edda')">
                                <td><strong>Mochamad Januardi</strong></td><td>Officer Inovasi</td><td><span class="status" style="background: #d4edda; color: #155724;">TKO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Nopiyanti', 'Officer PMSMT', 'TKNO', '#f8d7da')">
                                <td><strong>Nopiyanti</strong></td><td>Officer PMSMT</td><td><span class="status" style="background: #f8d7da; color: #721c24;">TKNO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Wahyu Sukmawati','VP PMSMT','TKO','#d4edda')">
                                <td><strong>Wahyu Sukmawati</strong></td><td>VP PMSMT</td><td><span class="status" style="background: #d4edda; color: #155724;">TKO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Putri Yunikeu', 'Officer Standardisasi', 'TKNO', '#f8d7da')">
                                <td><strong>Putri Yunikeu</strong></td><td>Officer Standardisasi</td><td><span class="status" style="background: #f8d7da; color: #721c24;">TKNO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Ari Citra Hermawan', 'Officer Paten & HAKI', 'TKO', '#d4edda')">
                                <td><strong>Ari Citra Hermawan</strong></td><td>Officer Paten & HAKI</td><td><span class="status" style="background: #d4edda; color: #155724;">TKO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Septian', 'Officer Digitalisasi', 'TKNO', '#f8d7da')">
                                <td><strong>Septian</strong></td><td>Officer Digitalisasi</td><td><span class="status" style="background: #f8d7da; color: #721c24;">TKNO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Dion Ridwan Giartomi', 'Officer Audit SMT', 'TKO', '#d4edda')">
                                <td><strong>Dion Ridwan Giartomi</strong></td><td>Officer Audit SMT</td><td><span class="status" style="background: #d4edda; color: #155724;">TKO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Yayan Sopyan', 'Officer 5R & Mutu', 'TKO', '#d4edda')">
                                <td><strong>Yayan Sopyan</strong></td><td>Officer 5R & Mutu</td><td><span class="status" style="background: #d4edda; color: #155724;">TKO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                            <tr onclick="viewDetail('Yunni Kusriwanti', 'Officer Administrasi Inovasi', 'TKNO', '#f8d7da')">
                                <td><strong>Yunni Kusriwanti</strong></td><td>Officer Administrasi Inovasi</td><td><span class="status" style="background: #f8d7da; color: #721c24;">TKNO</span></td>
                                <td><button class="action-btn btn-edit" onclick="event.stopPropagation(); editRow(this)"><i class="fas fa-edit"></i></button><button class="action-btn btn-delete" onclick="event.stopPropagation(); deleteRow(this)"><i class="fas fa-trash"></i></button></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div id="detail-karyawan" class="card">
                <button class="btn" onclick="backToList()" style="background: #64748b;"><i class="fas fa-arrow-left"></i> Kembali ke Daftar</button>
                <div class="profile-view">
                    <div class="avatar-big" id="p-avatar">?</div>
                    <h2 id="p-nama">Nama Karyawan</h2>
                    <p id="p-jabatan" style="color: #64748b; margin-bottom: 10px;">Jabatan</p>
                    <span id="p-status" class="status">Status</span>
                    
                    <div style="margin-top: 25px; text-align: left; background: var(--hover-color); padding: 20px; border-radius: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <p style="opacity: 0.7; font-size: 11px;">ID KARYAWAN</p>
                            <p><strong>PKC-SMTI-2026</strong></p>
                        </div>
                        <div>
                            <p style="opacity: 0.7; font-size: 11px;">EMAIL RESMI</p>
                            <p><strong id="p-email">user@pupuk-kujang.co.id</strong></p>
                        </div>
                        <div>
                            <p style="opacity: 0.7; font-size: 11px;">KOMPARTEMEN</p>
                            <p><strong>Sistem Manajemen Terpadu & Inovasi (SMTI)</strong></p>
                        </div>
                        <div>
                            <p style="opacity: 0.7; font-size: 11px;">PERUSAHAAN</p>
                            <p><strong>PT Pupuk Kujang Cikampek</strong></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= PAGE ANAK MAGANG / PKL ================= -->
        <div id="magang" class="page-section">
            <div class="header" style="margin-bottom: 16px;">
                <div class="header-left">
                    <div class="header-title">
                        <h1><i class="fas fa-user-graduate" style="color: #10b981;"></i> Data Mahasiswa & Siswa Magang / PKL</h1>
                        <small>Departemen Sistem Manajemen Terpadu & Inovasi (SMTI) - PT Pupuk Kujang</small>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <button class="btn" style="background: #10b981;" onclick="openAddInternModal()">
                        <i class="fas fa-user-plus"></i> + Tambah Anak Magang
                    </button>
                    <button class="btn" style="background: #0284c7;" onclick="openAddProjectModal()">
                        <i class="fas fa-project-diagram"></i> Buat Proyek Baru
                    </button>
                </div>
            </div>

            <!-- KPI Cards Magang -->
            <div class="dashboard-grid" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 20px;">
                <div class="card" style="margin: 0; padding: 16px; border-left: 4px solid #10b981;">
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748b;">Total Anak Magang</div>
                    <div style="font-size: 26px; font-weight: 800; color: var(--text-color); margin-top: 4px;" id="dash-magang-total">4</div>
                    <small style="color: #10b981; font-size: 11px;"><i class="fas fa-users"></i> Terdaftar di SMTI</small>
                </div>
                <div class="card" style="margin: 0; padding: 16px; border-left: 4px solid #0284c7;">
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748b;">Magang Aktif</div>
                    <div style="font-size: 26px; font-weight: 800; color: #0284c7; margin-top: 4px;" id="dash-magang-aktif">3</div>
                    <small style="color: #64748b; font-size: 11px;"><i class="fas fa-running"></i> Sedang Bertugas</small>
                </div>
                <div class="card" style="margin: 0; padding: 16px; border-left: 4px solid #64748b;">
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748b;">Magang Selesai (Alumni)</div>
                    <div style="font-size: 26px; font-weight: 800; color: #64748b; margin-top: 4px;" id="dash-magang-selesai">1</div>
                    <small style="color: #64748b; font-size: 11px;"><i class="fas fa-check-circle"></i> Selesai Periode</small>
                </div>
                <div class="card" style="margin: 0; padding: 16px; border-left: 4px solid #f59e0b;">
                    <div style="font-size: 11px; text-transform: uppercase; font-weight: 700; color: #64748b;">Asal Kampus / Sekolah</div>
                    <div style="font-size: 26px; font-weight: 800; color: #f59e0b; margin-top: 4px;" id="dash-magang-univ">4 Kampus</div>
                    <small style="color: #64748b; font-size: 11px;"><i class="fas fa-university"></i> ITB, UI, UNPAD, POLBAN</small>
                </div>
            </div>

            <!-- Table & Filter Magang -->
            <div class="card">
                <div class="filter-container" style="justify-content: space-between; align-items: center;">
                    <div style="display: flex; gap: 10px; flex: 1; flex-wrap: wrap;">
                        <input type="text" id="search-magang-input" class="filter-input" placeholder="🔍 Cari nama mahasiswa, jenis magang, kampus, atau penugasan..." oninput="filterInterns()">
                        <select id="type-magang-filter" class="filter-select" onchange="filterInterns()" style="font-weight: 600;">
                            <option value="">Semua Jenis Program Magang</option>
                            <option value="Magang Hub">🌐 Magang Hub</option>
                            <option value="MAGENTA">⚡ MAGENTA (BUMN)</option>
                            <option value="Magang Mandiri">🎓 Magang Mandiri</option>
                            <option value="PKL">🔧 PKL (Praktik Kerja Lapangan)</option>
                        </select>
                        <select id="status-magang-filter" class="filter-select" onchange="filterInterns()">
                            <option value="">Semua Status</option>
                            <option value="Aktif">Status: Aktif</option>
                            <option value="Selesai">Status: Selesai</option>
                        </select>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn btn-sm super-admin-only" id="btn-tambah-magang" style="background: #10b981;" onclick="openAddInternModal()">
                            <i class="fas fa-plus"></i> Tambah Anak Magang
                        </button>
                        <button class="btn btn-sm" style="background: #64748b;" onclick="exportInternsToCSV()">
                            <i class="fas fa-file-csv"></i> Export CSV
                        </button>
                    </div>
                </div>

                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Mahasiswa / Siswa Magang</th>
                                <th>Perguruan Tinggi & Jurusan</th>
                                <th>Penugasan / Minat SMTI</th>
                                <th>Periode Magang</th>
                                <th>Pembimbing SMTI</th>
                                <th>Status</th>
                                <th style="text-align: center;">Aksi</th>
                            </tr>
                        </thead>
                        <tbody id="intern-table-body">
                            <!-- Rendered dynamically by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ================= PAGE LAPORAN ANALYTICS ================= -->
        <div id="laporan" class="page-section">
            <div class="card">
                <div class="card-header">
                    <h2><i class="fas fa-chart-pie"></i> Laporan & Analytics Departemen SMTI</h2>
                    <button class="btn" onclick="alert('Laporan PDF berhasil di-generate!')"><i class="fas fa-download"></i> Unduh Laporan PDF</button>
                </div>
                <div class="dashboard-grid" style="margin-top: 15px;">
                    <div style="background: var(--hover-color); padding: 15px; border-radius: 8px;">
                        <h4>Rasio Status Karyawan</h4>
                        <p style="font-size: 22px; font-weight: bold; color: #0284c7; margin-top: 5px;">60% TKO / 40% TKNO</p>
                    </div>
                    <div style="background: var(--hover-color); padding: 15px; border-radius: 8px;">
                        <h4>Penyelesaian Proyek Inovasi</h4>
                        <p style="font-size: 22px; font-weight: bold; color: #16a34a; margin-top: 5px;">85.4% Target Triwulan</p>
                    </div>
                    <div style="background: var(--hover-color); padding: 15px; border-radius: 8px;">
                        <h4>Prosedur & IK Terbit</h4>
                        <p style="font-size: 22px; font-weight: bold; color: #d97706; margin-top: 5px;">36 Dokumen Resmi</p>
                    </div>
                </div>
                <div class="card-header" style="margin-top: 20px;"><span>Grafik Distribusi Beban Kerja & Evaluasi Inovasi</span></div>
                <div class="chart-container">
                    <canvas id="analyticsChart"></canvas>
                </div>
            </div>
        </div>

        <!-- ================= PAGE PENGATURAN ================= -->
        <div id="pengaturan" class="page-section">
            <div class="card">
                <h2 style="margin-bottom: 20px;"><i class="fas fa-sliders-h"></i> Pengaturan Sistem & Tampilan Monitor</h2>
                
                <div class="setting-group">
                    <div>
                        <strong>Pengingat Suara untuk Proyek Urgensi Tinggi</strong>
                        <p style="font-size: 12px; opacity: 0.7;">Bunyikan nada pengingat halus saat deadline mendekat H-3.</p>
                    </div>
                    <input type="checkbox" checked style="width: 20px; height: 20px; cursor: pointer;">
                </div>

                <div class="setting-group">
                    <div>
                        <strong>Penyimpanan Data Lokal (LocalStorage)</strong>
                        <p style="font-size: 12px; opacity: 0.7;">Simpan otomatis checklist manual dan komentar pengguna.</p>
                    </div>
                    <button class="btn btn-sm" style="background: #dc2626;" onclick="resetToDefaultData()">Reset Semua Data Proyek</button>
                </div>

                <div class="setting-group">
                    <div>
                        <strong>Notifikasi Email Deadline Proyek</strong>
                        <p style="font-size: 12px; opacity: 0.7;">Kirim email otomatis ke PIC saat ada perubahan status tahap kerja.</p>
                    </div>
                    <input type="checkbox" checked style="width: 20px; height: 20px; cursor: pointer;">
                </div>

                <div class="setting-group">
                    <div>
                        <strong>Bahasa Antarmuka</strong>
                        <p style="font-size: 12px; opacity: 0.7;">Pilih bahasa tampilan dashboard.</p>
                    </div>
                    <select class="filter-select">
                        <option>Bahasa Indonesia</option>
                        <option>English (US)</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- ================= PAGE BANTUAN ================= -->
        <div id="bantuan" class="page-section">
            <div class="card">
                <h2 style="margin-bottom: 20px;"><i class="fas fa-life-ring"></i> Pusat Panduan & Dukungan SMTI</h2>
                
                <h4 style="margin-bottom: 10px;">Pertanyaan Umum (FAQ)</h4>
                <div class="faq-item">
                    <div class="faq-title"><i class="fas fa-chevron-right"></i> Bagaimana cara menambah checklist manual dan komentar?</div>
                    <p style="font-size: 13px; opacity: 0.8;">Buka proyek yang diinginkan dengan mengklik kartunya. Pada bagian Checklist Kegiatan, ketik tugas/dokumen baru pada kolom input "+ Tambah kegiatan..." lalu klik tombol "Tambah" atau tekan Enter. Di bawahnya, Anda juga dapat mengetik pesan/catatan tim pada kolom komentar.</p>
                </div>

                <div class="faq-item">
                    <div class="faq-title"><i class="fas fa-chevron-right"></i> Bagaimana jika suatu tahapan kerja sudah selesai duluan?</div>
                    <p style="font-size: 13px; opacity: 0.8;">Di dalam modal flow terdapat tombol kendali status: Anda bisa langsung klik <strong>"Set Selesai"</strong> pada tahap manapun. Seluruh checklist pada tahap tersebut akan otomatis ditandai tuntas, atau Anda juga bisa mengatur persentase progres manual menggunakan kotak persentase di bagian atas modal.</p>
                </div>

                <div class="faq-item">
                    <div class="faq-title"><i class="fas fa-chevron-right"></i> Apakah perubahan data saya akan hilang jika browser di-refresh?</div>
                    <p style="font-size: 13px; opacity: 0.8;">Tidak. Semua penambahan checklist, centang tugas, komentar user, dan perubahan progres disimpan secara permanen di <strong>LocalStorage</strong> browser komputer Anda.</p>
                </div>
            </div>
        </div>

    </div>

    <!-- =========================================================
         OVERLAY KHUSUS: MODE MONITOR TV / PENGINGAT LAYAR
         ========================================================= -->
    <div id="monitor-overlay">
        <!-- Topbar Monitor -->
        <div class="monitor-topbar">
            <div class="monitor-brand">
                <div class="monitor-brand-icon">
                    <i class="fas fa-tv"></i>
                </div>
                <div class="monitor-brand-text">
                    <h1>MONITOR PROYEK & PENGINGAT DEADLINE <span class="monitor-live-tag">LIVE BOARD</span></h1>
                    <p>Departemen Sistem Manajemen Terpadu & Inovasi (SMTI) • PT Pupuk Kujang</p>
                </div>
            </div>

            <!-- Jam Digital Monitor Besar -->
            <div class="monitor-clock-box">
                <div class="monitor-clock-time" id="monitor-live-clock">--:--:-- WIB</div>
                <div class="monitor-clock-date" id="monitor-live-date">Rabu, 16 September 2026</div>
            </div>

            <!-- Kontrol Monitor -->
            <div class="monitor-controls">
                <button class="monitor-btn" onclick="toggleFullscreen()" title="Layar Penuh (F11)">
                    <i class="fas fa-expand"></i> Fullscreen
                </button>
                <button class="monitor-btn" onclick="toggleDarkMode()" title="Ganti Mode Gelap/Terang">
                    <i class="fas fa-adjust"></i> Tema
                </button>
                <button class="monitor-btn btn-close-monitor" onclick="closeMonitorMode()">
                    <i class="fas fa-times-circle"></i> Tutup Monitor
                </button>
            </div>
        </div>

        <!-- Ticker Berjalan Pengingat (Urgent Marquee) -->
        <div class="monitor-ticker-wrap">
            <div class="ticker-label">
                <i class="fas fa-bell"></i> PENGINGAT URGENT
            </div>
            <div class="ticker-marquee">
                <div class="ticker-track" id="monitor-ticker-content">
                    ⚠️ PENGINGAT URGENSI TINGGI: KIX Prototyping - 72.8% peserta belum mengisi form (Target Pitching: 15 Mei 2026) • 🚨 AUDIT ISO 27001: Persiapan tindak lanjut CAR temuan audit eksternal sedang berjalan! • ⚡ DIGITALISASI PABRIK: Uji coba lapangan Pabrik 1B untuk showcase HUT PKC! • 📌 ICCOSH: Konfirmasi berkas & daftar nama delegasi 3 gugus ke Yogyakarta!
                </div>
            </div>
        </div>

        <!-- Filter Bar Layar Monitor Interaktif -->
        <div class="monitor-filter-bar">
            <div class="monitor-filter-left">
                <span class="monitor-filter-title"><i class="fas fa-filter"></i> TAMPILKAN URGENSI:</span>
                <div class="monitor-filter-pills">
                    <button class="mon-pill-btn active" onclick="setMonitorUrgencyFilter('semua', this)" id="mon-btn-all" title="Tampilkan seluruh kolom tingkat urgensi (Tekan 1)">
                        <i class="fas fa-th-large"></i> Semua Kolom <span class="mon-pill-count" id="mon-pill-count-all">0</span>
                    </button>
                    <button class="mon-pill-btn mon-pill-high" onclick="setMonitorUrgencyFilter('Tinggi', this)" id="mon-btn-high" title="Hanya tampilkan Prioritas Utama (Tekan 2)">
                        <i class="fas fa-fire"></i> Urgensi Tinggi Saja <span class="mon-pill-count" id="mon-pill-count-high">0</span>
                    </button>
                    <button class="mon-pill-btn mon-pill-med" onclick="setMonitorUrgencyFilter('Sedang', this)" id="mon-btn-med" title="Hanya tampilkan Dalam Pengawalan (Tekan 3)">
                        <i class="fas fa-hourglass-half"></i> Urgensi Sedang Saja <span class="mon-pill-count" id="mon-pill-count-med">0</span>
                    </button>
                    <button class="mon-pill-btn mon-pill-low" onclick="setMonitorUrgencyFilter('Rendah', this)" id="mon-btn-low" title="Hanya tampilkan Rutin & Monitoring (Tekan 4)">
                        <i class="fas fa-check-circle"></i> Rutin Saja <span class="mon-pill-count" id="mon-pill-count-low">0</span>
                    </button>
                </div>
            </div>
            <div class="monitor-filter-right">
                <span class="monitor-filter-title"><i class="fas fa-layer-group"></i> BIDANG:</span>
                <select id="mon-cat-filter" onchange="setMonitorCategoryFilter(this.value)" class="mon-cat-select" title="Saring proyek berdasarkan bidang kerja">
                    <option value="semua">Semua Bidang (MIKU, PMSMT, PSP)</option>
                    <option value="MIKU">MIKU</option>
                    <option value="PMSMT">PMSMT</option>
                    <option value="Pengembangan Sistem dan Prosedur">Pengembangan Sistem & Prosedur</option>
                </select>
            </div>
        </div>

        <!-- 3-Column Urgency Board (Dynamic Filter Responsive) -->
        <div class="monitor-board">
            <!-- Kolom 1: Urgensi Tinggi -->
            <div class="monitor-column monitor-col-high" id="mon-col-high">
                <div class="monitor-col-header">
                    <h3><i class="fas fa-fire"></i> PRIORITAS UTAMA (URGENSI TINGGI)</h3>
                    <span class="monitor-col-badge" id="mon-count-high">3 Proyek</span>
                </div>
                <div class="monitor-card-list" id="monitor-list-high">
                    <!-- Dynamic -->
                </div>
            </div>

            <!-- Kolom 2: Urgensi Sedang -->
            <div class="monitor-column monitor-col-med" id="mon-col-med">
                <div class="monitor-col-header">
                    <h3><i class="fas fa-hourglass-half"></i> DALAM PENGAWALAN (URGENSI SEDANG)</h3>
                    <span class="monitor-col-badge" id="mon-count-med">3 Proyek</span>
                </div>
                <div class="monitor-card-list" id="monitor-list-med">
                    <!-- Dynamic -->
                </div>
            </div>

            <!-- Kolom 3: Rutin & Selesai -->
            <div class="monitor-column monitor-col-low" id="mon-col-low">
                <div class="monitor-col-header">
                    <h3><i class="fas fa-check-circle"></i> RUTIN & MONITORING</h3>
                    <span class="monitor-col-badge" id="mon-count-low">2 Proyek</span>
                </div>
                <div class="monitor-card-list" id="monitor-list-low">
                    <!-- Dynamic -->
                </div>
            </div>
        </div>
    </div>

    <!-- =========================================================
         MODAL ALUR PROGRES PROYEK (FLOW PIPELINE STEPPER)
         ========================================================= -->
    <div id="flowModal">
        <div class="flow-modal-box">
            <div class="flow-modal-header">
                <div>
                    <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 6px;">
                        <span id="modal-project-category" class="project-category-tag">Kategori</span>
                        <span id="modal-project-urgency" class="urgency-badge high">Urgensi Tinggi</span>
                        <span id="modal-project-status" class="status" style="background: rgba(2, 132, 199, 0.12); color: #0284c7;">In Progress</span>
                    </div>
                    <h2 id="modal-project-title">Nama Proyek</h2>
                    <p id="modal-project-desc" style="font-size: 13px; color: #64748b; line-height: 1.4;"></p>
                </div>
                <button class="flow-modal-close" onclick="closeFlowModal()">&times;</button>
            </div>

            <div class="flow-modal-body">
                <!-- Toolbar Cepat Pengatur Status Tahap & Manual Progress -->
                <div class="stage-control-toolbar">
                    <div class="stage-status-actions">
                        <span style="font-size: 12px; font-weight: 700; color: #64748b;"><i class="fas fa-sliders-h"></i> Atur Status Tahap Ini:</span>
                        <button class="stage-status-btn btn-set-completed" onclick="setStepStatusManually('completed')">
                            <i class="fas fa-check-double"></i> Set Selesai
                        </button>
                        <button class="stage-status-btn btn-set-active" onclick="setStepStatusManually('active')">
                            <i class="fas fa-play"></i> Set Berjalan (Aktif)
                        </button>
                        <button class="stage-status-btn btn-set-pending" onclick="setStepStatusManually('pending')">
                            <i class="fas fa-pause"></i> Set Menunggu
                        </button>
                    </div>

                    <div class="progress-manual-box">
                        <span>Total Progres:</span>
                        <input type="number" id="manual-progress-input" class="progress-manual-input" min="0" max="100" value="0">
                        <span>%</span>
                        <button class="btn btn-sm" onclick="applyManualProgress()"><i class="fas fa-save"></i> Terapkan</button>
                    </div>
                </div>

                <!-- Meta Highlights -->
                <div class="flow-meta-grid">
                    <div class="flow-meta-item">
                        <small>Target Deadline</small>
                        <strong id="modal-meta-deadline" style="color: #dc2626;">-</strong>
                    </div>
                    <div class="flow-meta-item">
                        <small>Penanggung Jawab (PIC)</small>
                        <strong id="modal-meta-pic">-</strong>
                    </div>
                    <div class="flow-meta-item">
                        <small>Total Progres</small>
                        <strong id="modal-meta-progress" style="color: #0284c7;">-</strong>
                    </div>
                    <div class="flow-meta-item">
                        <small>Posisi Tahap</small>
                        <strong id="modal-meta-stage">-</strong>
                    </div>
                </div>

                <!-- Tim & Karyawan Ter-invite ke Proyek -->
                <div class="project-team-section">
                    <div class="team-bar-left">
                        <span class="team-bar-label"><i class="fas fa-users"></i> Tim Proyek & Karyawan Ter-invite (<span id="modal-team-count">0</span>):</span>
                        <div class="team-avatars-list" id="modal-team-avatars-list">
                            <!-- Rendered by JS -->
                        </div>
                    </div>
                    <button type="button" class="btn btn-sm btn-invite-team" onclick="openInviteTeamModal()">
                        <i class="fas fa-user-plus"></i> + Undang Karyawan SMTI
                    </button>
                </div>

                <!-- Stepper Diagram Alur Kerja -->
                <div class="flow-stepper-container">
                    <div class="flow-stepper-title">
                        <span><i class="fas fa-sitemap"></i> Alur Tahapan Kerja (Workflow Flow)</span>
                        <small style="color: #64748b;">Klik lingkaran tahap untuk melihat dan mengedit tugas</small>
                    </div>

                    <div class="stepper-pipeline" id="modal-stepper-pipeline">
                        <!-- Rendered by JS -->
                    </div>
                </div>

                <!-- Detail Tahap yang Dipilih / Sedang Aktif -->
                <div class="active-stage-detail" id="modal-stage-detail-box">
                    <div class="stage-detail-header">
                        <div>
                            <span id="modal-active-stage-badge" class="stage-badge-current">Tahap 3 • Sedang Berjalan</span>
                            <h3 id="modal-active-stage-title" style="font-size: 16px; margin-top: 6px;">Pendampingan Peserta & Prototyping</h3>
                        </div>
                        <span id="modal-active-stage-date" style="font-size: 12px; font-weight: 700; color: #64748b;">16 Apr - 8 Mei 2026</span>
                    </div>

                    <p id="modal-active-stage-desc" style="font-size: 13.5px; line-height: 1.6;"></p>

                    <!-- Alert Box bila ada catatan kritis -->
                    <div class="stage-alert-box" id="modal-stage-alert" style="display: none;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <i class="fas fa-exclamation-triangle" style="font-size: 16px;"></i>
                            <span id="modal-stage-alert-text">Perhatian: Progres membutuhkan percepatan!</span>
                        </div>
                        <button class="btn btn-sm" style="background: rgba(220, 38, 38, 0.2); color: #dc2626;" onclick="editAlertNote()">
                            <i class="fas fa-pen"></i> Ubah Catatan
                        </button>
                    </div>

                    <!-- Checklist Kegiatan pada Tahap Tersebut -->
                    <div class="task-checklist">
                        <div class="task-checklist-header">
                            <h4><i class="fas fa-clipboard-check" style="color: #16a34a;"></i> Checklist Kegiatan / Dokumen Syarat:</h4>
                            <span style="font-size: 11px; opacity: 0.7;" id="checklist-summary-text">0/0 selesai</span>
                        </div>

                        <!-- Tasks checklist items container -->
                        <div id="modal-stage-checklist"></div>

                        <!-- Form Input Manual Tambah Checklist Baru -->
                        <form class="add-task-form" onsubmit="event.preventDefault(); addNewTask();">
                            <input type="text" id="new-task-input" class="add-task-input" placeholder="+ Ketik nama kegiatan / dokumen syarat baru lalu tekan Enter...">
                            <button type="submit" class="btn btn-sm" style="background: #16a34a;">
                                <i class="fas fa-plus"></i> Tambah
                            </button>
                        </form>
                    </div>
                </div>

                <!-- =========================================================
                     FORUM CHAT & KETERANGAN PROGRES TIM PROYEK SMTI
                     ========================================================= -->
                <div class="comments-section">
                    <div class="comments-header">
                        <div>
                            <h4><i class="fas fa-comments" style="color: #0284c7;"></i> Chat & Keterangan Progres Tim Proyek</h4>
                            <small style="color: #64748b;">Karyawan ter-invite dapat mengirim laporan progres, kendala, atau diskusi tahapan di bawah.</small>
                        </div>
                        <span class="comments-count-badge" id="comments-count-badge" style="background: rgba(2, 132, 199, 0.12); color: #0284c7; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 11px;">0 Pesan</span>
                    </div>

                    <!-- Feed Komentar / Chat Progres -->
                    <div class="comments-list" id="modal-comments-list">
                        <!-- Rendered by JS -->
                    </div>

                    <!-- Form Tambah Chat / Keterangan Progres -->
                    <form class="progress-chat-form" onsubmit="event.preventDefault(); addNewComment();">
                        <div style="display: flex; gap: 10px; margin-bottom: 8px; flex-wrap: wrap;">
                            <div style="flex: 1; min-width: 180px;">
                                <label style="font-size: 11px; font-weight: 700; color: #64748b; display: block; margin-bottom: 4px;">
                                    <i class="fas fa-user-check"></i> Kirim Sebagai (Karyawan SMTI):
                                </label>
                                <select id="comment-author-select" class="chat-select" style="width: 100%; padding: 7px 10px; border: 1px solid var(--border-color); border-radius: 6px; background: var(--card-bg); color: var(--text-color); font-size: 12px; font-weight: 600; outline: none;">
                                    <!-- Populated dynamically -->
                                </select>
                            </div>
                            <div style="flex: 1; min-width: 180px;">
                                <label style="font-size: 11px; font-weight: 700; color: #64748b; display: block; margin-bottom: 4px;">
                                    <i class="fas fa-tag"></i> Jenis Keterangan:
                                </label>
                                <select id="comment-tag-select" class="chat-select" style="width: 100%; padding: 7px 10px; border: 1px solid var(--border-color); border-radius: 6px; background: var(--card-bg); color: var(--text-color); font-size: 12px; font-weight: 600; outline: none;">
                                    <option value="progress">🚀 Update Progres Kerja</option>
                                    <option value="done">✅ Tahap / Checklist Selesai</option>
                                    <option value="issue">⚠️ Kendala / Hambatan</option>
                                    <option value="note">📌 Catatan / Koordinasi</option>
                                </select>
                            </div>
                        </div>
                        <div style="display: flex; gap: 8px; align-items: flex-end;">
                            <textarea id="new-comment-input" rows="2" class="comment-textarea" placeholder="Tulis rincian progres sudah sampai mana, pencapaian tugas, atau kendala..." style="flex: 1; padding: 10px 12px; border: 1px solid var(--border-color); border-radius: 8px; background: var(--card-bg); color: var(--text-color); font-size: 12.5px; outline: none; resize: none;"></textarea>
                            <button type="submit" class="btn" style="background: #0284c7; height: 50px; padding: 0 18px; font-weight: 700; display: flex; align-items: center; gap: 6px; white-space: nowrap;">
                                <i class="fas fa-paper-plane"></i> Kirim Chat
                            </button>
                        </div>
                    </form>
                </div>

                <div class="flow-modal-actions">
                    <div style="display: flex; gap: 8px;">
                        <button class="btn btn-sm" style="background: #16a34a; font-weight: 700;" onclick="markProjectCompletedQuick()" title="Langsung tandai seluruh tahapan dan proyek selesai 100%">
                            <i class="fas fa-check-double"></i> Tandai Selesai (100%)
                        </button>
                        <button class="btn btn-sm" style="background: #64748b;" onclick="copyProgressSummary()">
                            <i class="fas fa-copy"></i> Salin Ringkasan Progres
                        </button>
                        <button class="btn btn-sm" style="background: #e67e22;" onclick="reopenOrResetProject()">
                            <i class="fas fa-undo"></i> Buka Ulang / Reset Progres
                        </button>
                        <button class="btn btn-sm" style="background: #dc2626;" onclick="deleteProject(currentActiveProjectId)">
                            <i class="fas fa-trash-alt"></i> Hapus Proyek
                        </button>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn" style="background: #16a34a;" onclick="advanceStage()">
                            <i class="fas fa-forward"></i> Tahap Berikutnya
                        </button>
                        <button class="btn" onclick="closeFlowModal()">Tutup</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- =========================================================
         MODAL FORM TAMBAH PROYEK BARU (SCROLL HALUS & ALUR MANUAL)
         ========================================================= -->
    <div id="modalTambahProyek" class="modal">
        <div class="modal-content" style="width: 620px; max-width: 96%; max-height: 90vh; display: flex; flex-direction: column; overflow: hidden; padding: 0;">
            <!-- Pinned Header -->
            <div class="modal-header" style="padding: 16px 22px; margin: 0; border-bottom: 1px solid var(--border-color); background: var(--hover-color); display: flex; justify-content: space-between; align-items: center; flex-shrink: 0;">
                <h3 style="margin: 0; font-size: 16px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-project-diagram" style="color: #0284c7;"></i> Buat Proyek Baru SMTI
                </h3>
                <span class="close-modal" onclick="closeAddProjectModal()" style="font-size: 22px; cursor: pointer; color: #888;">&times;</span>
            </div>

            <!-- Form Container with Scrollable Body and Pinned Footer -->
            <form id="form-tambah-proyek" onsubmit="saveNewProject(event)" style="display: flex; flex-direction: column; flex: 1; min-height: 0; overflow: hidden; margin: 0;">
                <!-- Scrollable Body (Guarantees no elements cut off on laptop screen) -->
                <div style="overflow-y: auto; padding: 18px 22px; flex: 1; max-height: calc(90vh - 125px);">
                    <div class="form-group">
                        <label>Nama Proyek *</label>
                        <input type="text" id="new-proj-name" required placeholder="Contoh: Implementasi ISO 50001 Sistem Manajemen Energi">
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="form-group">
                            <label>Kategori Bagian / Bidang *</label>
                            <select id="new-proj-category" required>
                                <option value="MIKU">MIKU (Manajemen Inovasi & Kinerja Unggul)</option>
                                <option value="PMSMT">PMSMT (Pengendalian Manajemen SMT)</option>
                                <option value="Pengembangan Sistem dan Prosedur">Pengembangan Sistem dan Prosedur</option>
                                <option value="Proyek Riset & Inovasi Magang">Proyek Riset & Inovasi Magang</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Tingkat Urgensi *</label>
                            <select id="new-proj-urgency" required>
                                <option value="Tinggi">🔥 Urgensi Tinggi (Prioritas Utama)</option>
                                <option value="Sedang" selected>⏳ Urgensi Sedang (Pengawalan)</option>
                                <option value="Rendah">✅ Urgensi Rendah (Rutin)</option>
                            </select>
                        </div>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div class="form-group">
                            <label>Target Deadline *</label>
                            <input type="date" id="new-proj-deadline" required>
                        </div>
                        <div class="form-group">
                            <label>Penanggung Jawab (PIC) *</label>
                            <input type="text" id="new-proj-pic" list="pic-suggestions-list" required placeholder="Contoh: Dion / Tim SMTI">
                            <datalist id="pic-suggestions-list"></datalist>
                            <small style="color: #0284c7; font-size: 11px; margin-top: 4px; display: block;">
                                <i class="fas fa-magic"></i> Otomatis akun login Anda (dapat diganti jika menugaskan personil lain)
                            </small>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Deskripsi / Tujuan Proyek</label>
                        <textarea id="new-proj-desc" rows="2" placeholder="Jelaskan ringkasan tujuan atau latar belakang proyek..."></textarea>
                    </div>

                    <div class="form-group">
                        <label>Catatan Peringatan / Status Terkini (Opsional)</label>
                        <input type="text" id="new-proj-alert" placeholder="Contoh: Menunggu disposisi persetujuan memo direksi">
                    </div>

                    <div class="form-group">
                        <label><i class="fas fa-user-plus"></i> Undang Anggota Tim Karyawan SMTI:</label>
                        <div id="new-proj-team-select" style="display: flex; flex-wrap: wrap; gap: 6px; padding: 10px; background: var(--hover-color); border: 1px solid var(--border-color); border-radius: 8px; max-height: 120px; overflow-y: auto;">
                            <!-- Checkboxes for all SMTI employees -->
                        </div>
                    </div>

                    <!-- Workflow Template Selector (Manual Default + User Saved Templates) -->
                    <div class="form-group" style="background: var(--hover-color); padding: 12px 14px; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 14px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
                            <label style="margin: 0; font-weight: 700; font-size: 12.5px;">
                                <i class="fas fa-sitemap" style="color: #0284c7;"></i> Template Alur Kerja:
                            </label>
                            <button type="button" id="btn-del-custom-tpl" class="btn btn-sm" style="display: none; background: #dc2626; padding: 3px 8px; font-size: 11px;" onclick="deleteCurrentCustomTemplate()" title="Hapus template tersimpan yang sedang dipilih">
                                <i class="fas fa-trash-alt"></i> Hapus Template Ini
                            </button>
                        </div>
                        <select id="new-proj-template" onchange="onTemplateSelectChange(this.value)" style="width: 100%; padding: 8px 10px; border: 1px solid var(--border-color); border-radius: 6px; font-size: 12.5px; background: var(--card-bg); color: var(--text-color); font-weight: 600;">
                            <!-- Populated dynamically by JS -->
                        </select>
                        <small id="tpl-desc-hint" style="color: #64748b; font-size: 11px; display: block; margin-top: 5px;">
                            Alur kerja bebas disusun manual sesuai fakta lapangan. Anda bisa menyimpannya sebagai template baru kapan saja.
                        </small>
                    </div>

                    <!-- Interactive Dynamic Steps Builder -->
                    <div class="form-group" style="background: var(--card-bg); padding: 14px; border-radius: 8px; border: 1px solid var(--border-color);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 6px;">
                            <label style="margin: 0; font-weight: 700; font-size: 12.5px; display: flex; align-items: center; gap: 6px;">
                                <i class="fas fa-list-check" style="color: #16a34a;"></i> Susunan Tahapan Alur Kerja:
                            </label>
                            <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                                <button type="button" class="btn btn-sm" style="background: #10b981; padding: 4px 10px; font-size: 11.5px;" onclick="promptSaveCurrentStepsAsTemplate()" title="Simpan susunan alur ini sebagai template baru yang dapat dipilih kembali di masa mendatang">
                                    <i class="fas fa-bookmark"></i> Simpan Jadi Template
                                </button>
                                <button type="button" class="btn btn-sm" style="background: #0284c7; padding: 4px 10px; font-size: 11.5px;" onclick="addCustomStepRow()">
                                    <i class="fas fa-plus"></i> Tambah Tahap
                                </button>
                            </div>
                        </div>
                        <div id="custom-steps-list" style="display: flex; flex-direction: column; gap: 8px; max-height: 220px; overflow-y: auto; padding-right: 4px;">
                            <!-- Dynamic Step Rows with Move Up/Down and Delete -->
                        </div>
                        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed var(--border-color); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                            <small style="color: #64748b; font-size: 11px;">
                                * Sesuaikan nama tahap & target waktu. Gunakan tombol ▲ ▼ untuk mengatur urutan tahapan.
                            </small>
                        </div>
                    </div>

                    <!-- Optional Checkbox: Auto-Save as Template when creating project -->
                    <div style="margin-top: 10px; padding: 10px 12px; background: var(--hover-color); border: 1px dashed var(--border-color); border-radius: 6px;">
                        <label style="font-size: 12px; font-weight: 600; display: flex; align-items: center; gap: 8px; cursor: pointer; margin: 0;">
                            <input type="checkbox" id="check-save-template-on-create" onchange="document.getElementById('save-tpl-name-box').style.display = this.checked ? 'block' : 'none';">
                            <span><i class="fas fa-save" style="color: #10b981;"></i> Simpan juga alur ini sebagai Template Baru saat proyek dibuat</span>
                        </label>
                        <div id="save-tpl-name-box" style="display: none; margin-top: 8px;">
                            <input type="text" id="input-save-template-name" placeholder="Beri nama template (misal: Alur Uji Stabilitas Pabrik)..." style="width: 100%; padding: 7px 10px; border: 1px solid var(--border-color); border-radius: 5px; font-size: 12px; background: var(--card-bg); color: var(--text-color); outline: none;">
                        </div>
                    </div>
                </div>

                <!-- Pinned Footer Buttons (Always in view without zooming out) -->
                <div style="display: flex; gap: 10px; justify-content: flex-end; padding: 14px 22px; border-top: 1px solid var(--border-color); background: var(--card-bg); flex-shrink: 0;">
                    <button type="button" class="btn" style="background: #64748b;" onclick="closeAddProjectModal()">Batal</button>
                    <button type="submit" class="btn" style="background: #0284c7; font-weight: 700; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);">
                        <i class="fas fa-save"></i> Buat & Daftarkan Proyek
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal Form Tambah Karyawan -->
    <div id="modalKaryawan" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modal-title">Tambah Karyawan Baru</h3>
                <span class="close-modal" onclick="closeModal()">&times;</span>
            </div>
            <form id="form-karyawan" onsubmit="saveKaryawan(event)">
                <div class="form-group">
                    <label>Nama Karyawan</label>
                    <input type="text" id="input-nama" required placeholder="Contoh: Budi Santoso">
                </div>
                <div class="form-group">
                    <label>Jabatan</label>
                    <input type="text" id="input-jabatan" required placeholder="Contoh: Officer Inovasi">
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <select id="input-status" required>
                        <option value="TKO">TKO (Tenaga Kerja Operasional)</option>
                        <option value="TKNO">TKNO (Tenaga Kerja Non-Operasional)</option>
                    </select>
                </div>
                <button type="submit" class="btn" style="width: 100%; margin-top: 10px; justify-content: center;">Simpan Data</button>
            </form>
        </div>
    </div>

    <!-- Modal Ganti PIN Akun Pengguna -->
    <div id="modalChangePin" class="modal">
        <div class="modal-content" style="width: 400px; max-width: 95%;">
            <div class="modal-header">
                <h3 style="display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 700;">
                    <i class="fas fa-key" style="color: #f59e0b;"></i> Ganti PIN Keamanan Akun
                </h3>
                <span class="close-modal" onclick="closeChangePinModal()">&times;</span>
            </div>
            <form onsubmit="saveNewPin(event)" style="padding: 6px 0;">
                <div class="form-group">
                    <label>PIN Saat Ini *</label>
                    <input type="password" id="change-pin-old" maxlength="6" required placeholder="Masukkan PIN lama (default: 1234)">
                </div>
                <div class="form-group">
                    <label>PIN Baru (4-6 Digit Angka) *</label>
                    <input type="password" id="change-pin-new" maxlength="6" required placeholder="Contoh: 8899">
                </div>
                <div class="form-group">
                    <label>Konfirmasi PIN Baru *</label>
                    <input type="password" id="change-pin-confirm" maxlength="6" required placeholder="Ulangi PIN baru...">
                </div>
                <div id="change-pin-error" style="display: none; color: #dc2626; font-size: 12px; margin-bottom: 12px; font-weight: 600;"></div>
                <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 15px; border-top: 1px solid var(--border-color); padding-top: 12px;">
                    <button type="button" class="btn btn-sm" style="background: #64748b;" onclick="closeChangePinModal()">Batal</button>
                    <button type="submit" class="btn btn-sm" style="background: #16a34a; font-weight: 700;">
                        <i class="fas fa-save"></i> Simpan PIN Baru
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal Form Tambah / Edit Anak Magang -->
    <div id="modalMagang" class="modal">
        <div class="modal-content" style="width: 520px; max-width: 95%;">
            <div class="modal-header">
                <h3 id="modal-magang-title"><i class="fas fa-user-graduate" style="color: #10b981;"></i> Tambah Data Anak Magang / PKL</h3>
                <span class="close-modal" onclick="closeAddInternModal()">&times;</span>
            </div>
            <form id="form-magang" onsubmit="saveIntern(event)" style="padding: 16px 20px;">
                <input type="hidden" id="magang-edit-id" value="">
                <div class="form-group">
                    <label>Nama Lengkap Mahasiswa / Siswa *</label>
                    <input type="text" id="input-magang-nama" required placeholder="Contoh: Dimas Pratama">
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div class="form-group">
                        <label>Jenis Program Magang *</label>
                        <select id="input-magang-type" required style="font-weight: 600;">
                            <option value="Magang Hub">🌐 Magang Hub</option>
                            <option value="MAGENTA">⚡ MAGENTA (BUMN)</option>
                            <option value="Magang Mandiri" selected>🎓 Magang Mandiri</option>
                            <option value="PKL">🔧 PKL (Praktik Kerja Lapangan)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Asal Perguruan Tinggi / Sekolah *</label>
                        <input type="text" id="input-magang-campus" required placeholder="Contoh: ITB / UI / SMKN 1">
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div class="form-group">
                        <label>Program Studi / Jurusan</label>
                        <input type="text" id="input-magang-major" placeholder="Contoh: Teknik Kimia / Rekayasa Perangkat Lunak">
                    </div>
                    <div class="form-group">
                        <label>Periode Magang (Bulan/Tahun) *</label>
                        <input type="text" id="input-magang-period" required placeholder="Contoh: Feb 2026 - Agu 2026">
                    </div>
                </div>
                <div class="form-group">
                    <label>Penugasan / Bidang Magang SMTI *</label>
                    <input type="text" id="input-magang-role" required placeholder="Contoh: Magang Riset Inovasi & Nilai Tambah">
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div class="form-group">
                        <label>Status Magang *</label>
                        <select id="input-magang-status" required>
                            <option value="Aktif" selected>Aktif (Sedang Berjalan)</option>
                            <option value="Selesai">Selesai (Alumni)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Pembimbing Karyawan SMTI *</label>
                        <select id="input-magang-mentor" required>
                            <!-- Populated dynamically from SMTI_EMPLOYEES -->
                        </select>
                    </div>
                </div>

                <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 18px; border-top: 1px solid var(--border-color); padding-top: 12px;">
                    <button type="button" class="btn" style="background: #64748b;" onclick="closeAddInternModal()">Batal</button>
                    <button type="submit" class="btn" style="background: #10b981; font-weight: 700;">
                        <i class="fas fa-save"></i> Simpan Data Magang
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- JAVASCRIPT LOGIC -->
    <script>
        /* =========================================================
           DATA MASTER ANAK MAGANG / PKL SMTI (PERSISTENSI LOCALSTORAGE & CLOUD)
           ========================================================= */
        const defaultSMTIInterns = [
            {
                id: 101,
                name: "Dimas Pratama",
                type: "MAGENTA",
                campus: "Institut Teknologi Bandung (ITB)",
                major: "Teknik Kimia",
                role: "Magang Riset Formulasi & Inovasi",
                period: "Feb 2026 - Agu 2026",
                mentor: "Mochamad Januardi",
                status: "Aktif",
                color: "#7c3aed",
                initials: "DP"
            },
            {
                id: 102,
                name: "Adinda Putri Rahayu",
                type: "Magang Hub",
                campus: "Universitas Indonesia (UI)",
                major: "Sistem Informasi",
                role: "Magang Digitalisasi & Web Dashboard",
                period: "Mar 2026 - Jul 2026",
                mentor: "Septian",
                status: "Aktif",
                color: "#0284c7",
                initials: "AP"
            },
            {
                id: 103,
                name: "Rizky Firmansyah",
                type: "Magang Mandiri",
                campus: "Universitas Padjadjaran (UNPAD)",
                major: "Manajemen Bisnis",
                role: "Magang Audit Mutu & Standardisasi",
                period: "Jan 2026 - Jun 2026",
                mentor: "Dion Ridwan Giartomi",
                status: "Aktif",
                color: "#059669",
                initials: "RF"
            },
            {
                id: 104,
                name: "Siti Nurhaliza",
                type: "PKL",
                campus: "SMKN 1 Karawang",
                major: "Teknik Kimia Industri",
                role: "PKL Operasional Pabrik & 5R",
                period: "Feb 2026 - Mei 2026",
                mentor: "Yayan Sopyan",
                status: "Selesai",
                color: "#d97706",
                initials: "SN"
            }
        ];

        let SMTI_INTERNS = [];

        function loadInternsData() {
            try {
                const stored = localStorage.getItem('smti_interns_data_v1');
                if (stored) {
                    SMTI_INTERNS = JSON.parse(stored);
                } else {
                    SMTI_INTERNS = JSON.parse(JSON.stringify(defaultSMTIInterns));
                }
            } catch (e) {
                console.error("Gagal load interns:", e);
                SMTI_INTERNS = JSON.parse(JSON.stringify(defaultSMTIInterns));
            }
            // Pastikan setiap record memiliki jenis program magang (migrasi data lama)
            SMTI_INTERNS.forEach(intern => {
                if (!intern.type) {
                    const def = defaultSMTIInterns.find(d => d.name.toLowerCase() === intern.name.toLowerCase());
                    intern.type = def ? def.type : "Magang Mandiri";
                }
            });

            renderInternsTable();
            updateInternsCount();
        }

        function saveInternsData() {
            try {
                localStorage.setItem('smti_interns_data_v1', JSON.stringify(SMTI_INTERNS));
            } catch (e) {
                console.error("Gagal save interns:", e);
            }

            renderInternsTable();
            updateInternsCount();
            populateNewProjectMemberCheckboxes();

            if (typeof currentActiveProjectId !== 'undefined' && currentActiveProjectId) {
                const curProj = projectDataSMTI.find(p => p.id === currentActiveProjectId);
                if (curProj) {
                    renderProjectTeam(curProj);
                    populateChatAuthorSelect(curProj);
                }
            }

            clearTimeout(window.syncInternsTimeout);
            window.syncInternsTimeout = setTimeout(syncInternsToCloud, 700);
        }

        const VERCEL_INTERNS_ENDPOINT = (window.location.hostname.includes('localhost') || window.location.hostname.includes('127.0.0.1'))
            ? 'https://smti-pupuk-kujang.vercel.app/api/interns'
            : '/api/interns';

        async function syncInternsToCloud() {
            try {
                const res = await fetch(VERCEL_INTERNS_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(SMTI_INTERNS)
                });
                if (res.ok) {
                    console.log("Data anak magang berhasil disinkronkan ke Vercel Cloud.");
                }
            } catch (e) {
                console.warn("Gagal sinkron data magang ke cloud:", e);
            }
        }

        async function fetchInternsFromCloud() {
            try {
                const res = await fetch(VERCEL_INTERNS_ENDPOINT);
                if (res.ok) {
                    const json = await res.json();
                    if (json && json.success && Array.isArray(json.data) && json.data.length > 0) {
                        SMTI_INTERNS = json.data;
                        // Pastikan tipe terisi jika belum ada di data cloud lama
                        SMTI_INTERNS.forEach(intern => {
                            if (!intern.type) {
                                const def = defaultSMTIInterns.find(d => d.name.toLowerCase() === intern.name.toLowerCase());
                                intern.type = def ? def.type : "Magang Mandiri";
                            }
                        });
                        localStorage.setItem('smti_interns_data_v1', JSON.stringify(SMTI_INTERNS));
                        renderInternsTable();
                        updateInternsCount();
                        populateNewProjectMemberCheckboxes();
                    }
                }
            } catch (e) {
                console.warn("Offline / tidak dapat fetch cloud interns:", e);
            }
        }

        function updateInternsCount() {
            const total = SMTI_INTERNS.length;
            const aktif = SMTI_INTERNS.filter(i => (i.status || 'Aktif') === 'Aktif').length;
            const selesai = SMTI_INTERNS.filter(i => i.status === 'Selesai').length;
            const campuses = new Set(SMTI_INTERNS.map(i => i.campus.trim())).size;

            if (document.getElementById('dash-magang-total')) document.getElementById('dash-magang-total').innerText = total;
            if (document.getElementById('dash-magang-aktif')) document.getElementById('dash-magang-aktif').innerText = aktif;
            if (document.getElementById('dash-magang-selesai')) document.getElementById('dash-magang-selesai').innerText = selesai;
            if (document.getElementById('dash-magang-univ')) document.getElementById('dash-magang-univ').innerText = `${campuses} Kampus`;
            if (document.getElementById('side-magang-count')) document.getElementById('side-magang-count').innerText = aktif;
        }

        function getInternTypeBadgeInfo(type) {
            const map = {
                'Magang Hub': { bg: 'rgba(2, 132, 199, 0.12)', color: '#0284c7', border: 'rgba(2, 132, 199, 0.35)', icon: 'fa-network-wired', label: 'Magang Hub' },
                'MAGENTA': { bg: 'rgba(124, 58, 237, 0.12)', color: '#7c3aed', border: 'rgba(124, 58, 237, 0.35)', icon: 'fa-bolt', label: 'MAGENTA' },
                'Magang Mandiri': { bg: 'rgba(16, 185, 129, 0.12)', color: '#059669', border: 'rgba(16, 185, 129, 0.35)', icon: 'fa-user-graduate', label: 'Magang Mandiri' },
                'PKL': { bg: 'rgba(217, 119, 6, 0.12)', color: '#d97706', border: 'rgba(217, 119, 6, 0.35)', icon: 'fa-tools', label: 'PKL' }
            };
            return map[type] || { bg: 'rgba(16, 185, 129, 0.12)', color: '#059669', border: 'rgba(16, 185, 129, 0.35)', icon: 'fa-graduation-cap', label: type || 'Magang' };
        }
        function renderInternsTable() {
            const table = document.getElementById('intern-table-body');
            if (!table) return;

            table.innerHTML = SMTI_INTERNS.map(intern => {
                const isAktif = (intern.status || 'Aktif') === 'Aktif';
                const statusColor = isAktif ? '#dcfce7' : '#f1f5f9';
                const statusTextColor = isAktif ? '#15803d' : '#475569';
                const typeInfo = getInternTypeBadgeInfo(intern.type);

                return `
                    <tr>
                        <td>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="background: ${intern.color || '#10b981'}; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 12px; border: 2px solid ${typeInfo.color}; flex-shrink: 0;">
                                    ${intern.initials || intern.name.slice(0, 2).toUpperCase()}
                                </div>
                                <div>
                                    <strong style="color: var(--text-color); font-size: 13.5px;">${intern.name}</strong>
                                    <div style="margin-top: 3px;">
                                        <span style="display: inline-flex; align-items: center; gap: 4px; font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 12px; background: ${typeInfo.bg}; color: ${typeInfo.color}; border: 1px solid ${typeInfo.border};">
                                            <i class="fas ${typeInfo.icon}"></i> ${typeInfo.label}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </td>
                        <td>
                            <strong>${intern.campus}</strong>
                            <div style="font-size: 11.5px; color: #64748b;">${intern.major || '-'}</div>
                        </td>
                        <td>${intern.role}</td>
                        <td><span style="font-size: 12px; color: var(--text-color);">${intern.period || '-'}</span></td>
                        <td><span style="background: var(--hover-color); padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;"><i class="fas fa-user-tie" style="color: #0284c7;"></i> ${intern.mentor || 'Tim SMTI'}</span></td>
                        <td><span class="status" style="background: ${statusColor}; color: ${statusTextColor}; font-weight: 700;">${intern.status || 'Aktif'}</span></td>
                        <td style="text-align: center; white-space: nowrap;">
                            ${isCurrentUserSuperAdmin() ? `
                                <button class="action-btn btn-edit" title="Edit anak magang" onclick="editInternById(${intern.id})"><i class="fas fa-edit"></i></button>
                                <button class="action-btn btn-delete" title="Hapus anak magang" onclick="deleteInternById(${intern.id})"><i class="fas fa-trash"></i></button>
                            ` : `
                                <span style="font-size: 11px; color: #94a3b8; font-style: italic;"><i class="fas fa-lock"></i> Terkunci</span>
                            `}
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function filterInterns() {
            const search = (document.getElementById('search-magang-input')?.value || '').toLowerCase();
            const typeFilter = (document.getElementById('type-magang-filter')?.value || '').toLowerCase();
            const status = (document.getElementById('status-magang-filter')?.value || '').toLowerCase();
            const rows = document.querySelectorAll('#intern-table-body tr');

            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                const matchSearch = search === '' || text.includes(search);
                const matchType = typeFilter === '' || text.includes(typeFilter);
                const matchStatus = status === '' || text.includes(status);
                row.style.display = (matchSearch && matchType && matchStatus) ? '' : 'none';
            });
        }

        function openAddInternModal(editId = null) {
            if (!isCurrentUserSuperAdmin()) {
                alert("Akses Terbatas: Hanya Super Admin (Septian) yang dapat menambah atau mengedit data anak magang.");
                return;
            }
            document.getElementById('form-magang').reset();
            document.getElementById('magang-edit-id').value = editId || '';

            // Populate Mentor Dropdown from SMTI_EMPLOYEES
            const mentorSelect = document.getElementById('input-magang-mentor');
            if (mentorSelect) {
                mentorSelect.innerHTML = SMTI_EMPLOYEES.map(e => `
                    <option value="${e.name}">${e.name} (${e.role})</option>
                `).join('');
            }

            if (editId) {
                const intern = SMTI_INTERNS.find(i => i.id == editId);
                if (intern) {
                    document.getElementById('modal-magang-title').innerHTML = `<i class="fas fa-edit" style="color: #10b981;"></i> Edit Data Anak Magang / PKL`;
                    document.getElementById('input-magang-nama').value = intern.name;
                    document.getElementById('input-magang-type').value = intern.type || 'Magang Mandiri';
                    document.getElementById('input-magang-campus').value = intern.campus;
                    document.getElementById('input-magang-major').value = intern.major || '';
                    document.getElementById('input-magang-role').value = intern.role;
                    document.getElementById('input-magang-period').value = intern.period;
                    document.getElementById('input-magang-status').value = intern.status;
                    if (mentorSelect) mentorSelect.value = intern.mentor;
                }
            } else {
                document.getElementById('modal-magang-title').innerHTML = `<i class="fas fa-user-graduate" style="color: #10b981;"></i> Tambah Data Anak Magang / PKL`;
                document.getElementById('input-magang-type').value = 'Magang Mandiri';
            }

            document.getElementById('modalMagang').style.display = 'flex';
        }

        function closeAddInternModal() {
            document.getElementById('modalMagang').style.display = 'none';
        }

        function saveIntern(e) {
            e.preventDefault();
            if (!isCurrentUserSuperAdmin()) {
                alert("Akses Terbatas: Hanya Super Admin (Septian) yang dapat menyimpan data anak magang.");
                return;
            }
            const editId = document.getElementById('magang-edit-id').value;
            const nama = document.getElementById('input-magang-nama').value.trim();
            const type = document.getElementById('input-magang-type').value;
            const campus = document.getElementById('input-magang-campus').value.trim();
            const major = document.getElementById('input-magang-major').value.trim();
            const role = document.getElementById('input-magang-role').value.trim();
            const period = document.getElementById('input-magang-period').value.trim();
            const status = document.getElementById('input-magang-status').value;
            const mentor = document.getElementById('input-magang-mentor').value;

            if (!nama || !campus || !role) return;

            const words = nama.split(' ');
            const initials = words.length > 1 ? (words[0][0] + words[1][0]).toUpperCase() : nama.slice(0, 2).toUpperCase();
            
            // Pilih warna avatar selaras dengan jenis program
            const colorByType = {
                'MAGENTA': '#7c3aed',
                'Magang Hub': '#0284c7',
                'Magang Mandiri': '#059669',
                'PKL': '#d97706'
            };
            const color = colorByType[type] || '#10b981';

            if (editId) {
                const intern = SMTI_INTERNS.find(i => i.id == editId);
                if (intern) {
                    intern.name = nama;
                    intern.type = type;
                    intern.campus = campus;
                    intern.major = major;
                    intern.role = role;
                    intern.period = period;
                    intern.status = status;
                    intern.mentor = mentor;
                    intern.initials = initials;
                    intern.color = color;
                }
            } else {
                const newIntern = {
                    id: Date.now(),
                    name: nama,
                    type: type,
                    campus: campus,
                    major: major,
                    role: role,
                    period: period,
                    mentor: mentor,
                    status: status,
                    color: color,
                    initials: initials
                };
                SMTI_INTERNS.push(newIntern);
            }

            saveInternsData();
            closeAddInternModal();
            filterInterns();
            alert(`Sukses! Data peserta magang "${nama}" (${type} - ${campus}) berhasil disimpan.`);
        }

        function editInternById(id) {
            openAddInternModal(id);
        }

        function deleteInternById(id) {
            if (!isCurrentUserSuperAdmin()) {
                alert("Akses Terbatas: Hanya Super Admin (Septian) yang dapat menghapus data anak magang.");
                return;
            }
            const intern = SMTI_INTERNS.find(i => i.id == id);
            if (!intern) return;

            if (confirm(`Hapus data anak magang "${intern.name}" (${intern.campus})? Data akan terhapus secara permanen.`)) {
                SMTI_INTERNS = SMTI_INTERNS.filter(i => i.id != id);
                saveInternsData();
                filterInterns();
                alert(`Data anak magang "${intern.name}" berhasil dihapus.`);
            }
        }

        function exportInternsToCSV() {
            let csv = ['Nama,Jenis Program,Kampus,Jurusan,Penugasan SMTI,Periode,Pembimbing,Status'];
            SMTI_INTERNS.forEach(i => {
                csv.push(`"${i.name}","${i.type || 'Magang Mandiri'}","${i.campus}","${i.major || '-'}","${i.role}","${i.period}","${i.mentor}","${i.status}"`);
            });
            const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'daftar_anak_magang_SMTI.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }

        /* =========================================================
           DATA MASTER KARYAWAN SMTI (PERSISTENSI LOCALSTORAGE & CLOUD)
           ========================================================= */
        const defaultSMTIEmployees = [
            { id: 1, name: "Henisya Permata Sari", role: "Manager Dept SMTI", status: "TKO", color: "#8b5cf6", initials: "HP", pin: "1234", isManager: true },
            { id: 2, name: "Mochamad Januardi", role: "Officer Inovasi", status: "TKO", color: "#3b82f6", initials: "MJ", pin: "1234" },
            { id: 3, name: "Septian", role: "Super Admin & Officer Digitalisasi", status: "TKNO", color: "#06b6d4", initials: "SP", pin: "1234", isSuperAdmin: true },
            { id: 4, name: "Dion Ridwan Giartomi", role: "Officer Audit SMT", status: "TKO", color: "#10b981", initials: "DR", pin: "1234" },
            { id: 5, name: "Wahyu Sukmawati", role: "VP PMSMT", status: "TKO", color: "#ec4899", initials: "WS", pin: "1234" },
            { id: 6, name: "Nopiyanti", role: "Officer PMSMT", status: "TKNO", color: "#f59e0b", initials: "NP", pin: "1234" },
            { id: 7, name: "Putri Yunikeu", role: "Officer Standardisasi", status: "TKNO", color: "#14b8a6", initials: "PY", pin: "1234" },
            { id: 8, name: "Ari Citra Hermawan", role: "Officer Paten & HAKI", status: "TKO", color: "#6366f1", initials: "AC", pin: "1234" },
            { id: 9, name: "Yayan Sopyan", role: "Officer 5R & Mutu", status: "TKO", color: "#84cc16", initials: "YS", pin: "1234" },
            { id: 10, name: "Yunni Kusriwanti", role: "Officer Administrasi Inovasi", status: "TKNO", color: "#f97316", initials: "YK", pin: "1234" }
        ];

        let SMTI_EMPLOYEES = [];

        function loadEmployeesData() {
            try {
                const stored = localStorage.getItem('smti_employees_data_v2');
                if (stored) {
                    SMTI_EMPLOYEES = JSON.parse(stored);
                } else {
                    SMTI_EMPLOYEES = JSON.parse(JSON.stringify(defaultSMTIEmployees));
                }
            } catch (e) {
                console.error("Gagal load employees dari localStorage:", e);
                SMTI_EMPLOYEES = JSON.parse(JSON.stringify(defaultSMTIEmployees));
            }

            // Sinkronkan peran khusus Henisya Permata Sari (Manager Dept SMTI) & Septian (Super Admin)
            SMTI_EMPLOYEES.forEach(emp => {
                if (emp.name.toLowerCase().includes('henisya')) {
                    emp.role = "Manager Dept SMTI";
                    emp.isManager = true;
                }
                if (emp.name.toLowerCase().includes('septian')) {
                    emp.role = "Super Admin & Officer Digitalisasi";
                    emp.isSuperAdmin = true;
                }
                if (!emp.pin) {
                    emp.pin = "1234";
                }
            });

            renderEmployeesTable();
            updateTotalCount();
        }

        function saveEmployeesData() {
            try {
                localStorage.setItem('smti_employees_data_v2', JSON.stringify(SMTI_EMPLOYEES));
            } catch (e) {
                console.error("Gagal simpan employees ke localStorage:", e);
            }

            renderEmployeesTable();
            updateTotalCount();
            populateNewProjectMemberCheckboxes();

            if (typeof currentActiveProjectId !== 'undefined' && currentActiveProjectId) {
                const curProj = projectDataSMTI.find(p => p.id === currentActiveProjectId);
                if (curProj) {
                    renderTeamAvatars(curProj);
                    renderCommentAuthorSelect(curProj);
                }
            }

            // Sinkronisasi otomatis ke Vercel Edge Config Cloud
            clearTimeout(window.syncEmployeesTimeout);
            window.syncEmployeesTimeout = setTimeout(syncEmployeesToCloud, 700);
        }

        const VERCEL_EMPLOYEES_ENDPOINT = (window.location.hostname.includes('localhost') || window.location.hostname.includes('127.0.0.1'))
            ? 'https://smti-pupuk-kujang.vercel.app/api/employees'
            : '/api/employees';

        async function syncEmployeesToCloud() {
            try {
                const res = await fetch(VERCEL_EMPLOYEES_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(SMTI_EMPLOYEES)
                });
                if (res.ok) {
                    console.log("Data karyawan berhasil disinkronkan ke Vercel Cloud.");
                }
            } catch (e) {
                console.warn("Gagal sinkron data karyawan ke cloud:", e);
            }
        }

        async function fetchEmployeesFromCloud() {
            try {
                const res = await fetch(VERCEL_EMPLOYEES_ENDPOINT);
                if (res.ok) {
                    const json = await res.json();
                    if (json && json.success && Array.isArray(json.data) && json.data.length > 0) {
                        SMTI_EMPLOYEES = json.data;
                        localStorage.setItem('smti_employees_data_v2', JSON.stringify(SMTI_EMPLOYEES));
                        renderEmployeesTable();
                        updateTotalCount();
                        populateNewProjectMemberCheckboxes();
                    }
                }
            } catch (e) {
                console.warn("Offline / tidak dapat fetch cloud employees:", e);
            }
        }

        /* =========================================================
           DATA MASTER PROYEK (Dengan Default & LocalStorage Persistence)
           ========================================================= */
        const defaultProjectDataSMTI = [
            {
                id: 1,
                name: "KIX - Prototyping and Pitch Preparation",
                category: "MIKU",
                teamMembers: ["Mochamad Januardi", "Henisya Permata Sari", "Yunni Kusriwanti"],
                urgency: "Tinggi",
                status: "In Progress",
                progress: 27,
                deadline: "15 Mei 2026",
                daysLeft: "H-3 Hari",
                pic: "Mochamad Januardi / Tim MIKU",
                description: "Pendampingan intensif peserta internal PKC dan 4 anak perusahaan (PT KIKC, PT WKS, PT SKP, PT Hurip Utama) dalam penyusunan prototipe dan proposal pitching inovasi KIX.",
                alertNote: "Perhatian Kritis: Realisasi pengisian formulir inovasi baru mencapai 27.2%, butuh asistensi langsung ke masing-masing gugus!",
                comments: [
                    { id: 1, author: "Mochamad Januardi", role: "PIC Inovasi", time: "16 Sep 2026, 09:30 WIB", text: "Sosialisasi internal dan anak perusahaan telah selesai. Saat ini fokus asistensi 1-on-1 ke gugus pabrik." },
                    { id: 2, author: "Henisya Permata Sari", role: "VP SMTI", time: "16 Sep 2026, 11:15 WIB", text: "Mohon segera dorong unit kerja yang persentasenya masih 0% agar pitching tanggal 15 Mei tidak terhambat." }
                ],
                flow: [
                    { stepNumber: 1, title: "Sosialisasi Internal", date: "1-2 Apr 2026", status: "completed", desc: "Sosialisasi panduan KIX secara daring & luring ke seluruh unit kerja PT Pupuk Kujang.", tasks: [["Materi panduan KIX terdistribusi", true], ["Sesi Q&A peserta selesai", true]] },
                    { stepNumber: 2, title: "Sosialisasi Afiliasi", date: "3-15 Apr 2026", status: "completed", desc: "Sosialisasi ke anak perusahaan (KIKC, WKS, SKP, Hurip Utama) untuk menjaring ide inovasi.", tasks: [["Roadshow anak perusahaan", true], ["Pendaftaran akun peserta afiliasi", true]] },
                    { stepNumber: 3, title: "Pendampingan & Prototyping", date: "16 Apr - 8 Mei 2026", status: "active", desc: "Monitoring progres pengisian formulir inovasi dan pembuatan mock-up / prototype produk inovasi.", tasks: [["Asistensi formulir inovasi (Saat ini: 27.2%)", false], ["Review kelayakan teknis prototype", false], ["Verifikasi kesiapan data pendukung", true]] },
                    { stepNumber: 4, title: "Pitch Preparation & Review", date: "9-12 Mei 2026", status: "pending", desc: "Coaching teknik pitching, penyusunan slide presentasi ringkas, dan simulasi penjurian.", tasks: [["Review slide presentasi 5 menit", false], ["Simulasi tanya jawab dewan juri", false]] },
                    { stepNumber: 5, title: "Final Pitching KIX", date: "15 Mei 2026", status: "pending", desc: "Presentasi di hadapan Dewan Juri dan Direksi untuk penetapan pemenang KIX 2026.", tasks: [["Pelaksanaan pitch day", false], ["Penetapan inovasi unggulan implementasi", false]] }
                ]
            },
            {
                id: 2,
                name: "Digitalisasi & Value Creation Pabrik (HUT PKC)",
                category: "MIKU",
                teamMembers: ["Septian", "Henisya Permata Sari"],
                urgency: "Tinggi",
                status: "In Progress",
                progress: 65,
                deadline: "31 Mei 2026",
                daysLeft: "H-18 Hari",
                pic: "Septian / Kompartemen Operasi",
                description: "Inisiatif inovasi digitalisasi operasional Pabrik 1A, Pabrik 1B, dan Pabrik NPK untuk efisiensi energi dan peningkatan EBITDA yang akan diluncurkan pada peringatan HUT Pupuk Kujang.",
                alertNote: "Arahan Direktur Utama: Fokus pada estimasi penghematan energi dan kesiapan live dashboard saat HUT!",
                comments: [
                    { id: 1, author: "Septian", role: "Officer Digitalisasi", time: "16 Sep 2026, 10:00 WIB", text: "Integrasi DCS Pabrik 1B sudah berjalan 80%. Sedang kalibrasi sensor konsumsi steam." }
                ],
                flow: [
                    { stepNumber: 1, title: "Rakor Bersama Dirut", date: "22 & 29 Apr 2026", status: "completed", desc: "Penyelarasan arahan Direktur Utama terkait fokus efisiensi dan kesiapan modul digitalisasi.", tasks: [["Notulen arahan Dirut", true], ["Penetapan KPI efisiensi", true]] },
                    { stepNumber: 2, title: "Blueprint Pabrik 1A & NPK", date: "4-5 Mei 2026", status: "completed", desc: "Penyusunan arsitektur pengumpulan data telemetry dan parameter produksi.", tasks: [["Integrasi sensor DCS/SCADA", true], ["Validasi data real-time", true]] },
                    { stepNumber: 3, title: "Uji Coba Pabrik 1B", date: "6-18 Mei 2026", status: "active", desc: "Uji coba monitoring performa operasional pabrik 1B secara terpusat.", tasks: [["Pengujian kestabilan koneksi", true], ["Uji akurasi kalkulasi efisiensi", false], ["Training operator konsol", false]] },
                    { stepNumber: 4, title: "Validasi EBITDA & Keuangan", date: "19-25 Mei 2026", status: "pending", desc: "Perhitungan nilai tambah finansial bersama bagian Akuntansi Manajemen.", tasks: [["Kajian dampak biaya energi", false], ["Penyusunan laporan value creation", false]] },
                    { stepNumber: 5, title: "Showcase HUT Pupuk Kujang", date: "31 Mei 2026", status: "pending", desc: "Peluncuran resmi sistem digitalisasi saat upacara/resepsi HUT PT Pupuk Kujang.", tasks: [["Live demo di hadapan Dewan Direksi", false], ["Serah terima operasional sistem", false]] }
                ]
            },
            {
                id: 3,
                name: "Audit Eksternal ISO 27001 & SMT (Sistem Manajemen Terintegrasi)",
                category: "PMSMT",
                teamMembers: ["Dion Ridwan Giartomi", "Wahyu Sukmawati"],
                urgency: "Tinggi",
                status: "In Progress",
                progress: 80,
                deadline: "20 Agustus 2026",
                daysLeft: "H-8 Hari",
                pic: "Dion Ridwan Giartomi / Tim PMSMT",
                description: "Sertifikasi Sistem Manajemen Keamanan Informasi (ISO 27001:2022) dan surveillance audit Sistem Manajemen Terintegrasi (ISO 9001, 14001, 45001, 50001, SMK3).",
                alertNote: "Batas Waktu CAR: Penyelesaian tindak lanjut temuan audit tahap 1 wajib diunggah sebelum audit final!",
                comments: [
                    { id: 1, author: "Dion Ridwan", role: "Officer Audit", time: "16 Sep 2026, 08:45 WIB", text: "CAR minor nomor 2 terkait log akses server sudah dilengkapi SOP tambahannya." }
                ],
                flow: [
                    { stepNumber: 1, title: "Rapat Pembahasan Isu ISO", date: "17 Juli 2026", status: "completed", desc: "Identifikasi isu internal/eksternal dan kebutuhan pihak berkepentingan (ISO 9001, 50001 & 14001).", tasks: [["Matriks konteks organisasi disetujui", true], ["Kajian risiko keamanan informasi", true]] },
                    { stepNumber: 2, title: "Penyisiran Lapangan & Server", date: "20 Juli 2026", status: "completed", desc: "Pemeriksaan fisik perlindungan ruang server (IK-0018) dan instalasi pabrik.", tasks: [["Checklist fisik ruang server aman", true], ["Verifikasi izin kerja panas/ruang terbatas", true]] },
                    { stepNumber: 3, title: "Audit Eksternal SMT Tahap 1", date: "27-31 Juli 2026", status: "completed", desc: "Pelaksanaan audit surveillance oleh auditor badan sertifikasi independen.", tasks: [["Opening & closing meeting selesai", true], ["Penerbitan daftar Corrective Action (CAR)", true]] },
                    { stepNumber: 4, title: "Roadshow Tindak Lanjut CAR", date: "1-18 Ags 2026", status: "active", desc: "Sosialisasi perbaikan dokumen dan implementasi tindakan korektif ke unit kerja pabrik.", tasks: [["Pemenuhan 3 CAR minor", true], ["Verifikasi efektivitas tindakan perbaikan", false]] },
                    { stepNumber: 5, title: "Audit Final ISO 27001", date: "19-20 Ags 2026", status: "pending", desc: "Audit tahap akhir untuk rekomendasi penerbitan sertifikat ISO 27001:2022.", tasks: [["Audit substantif sistem keamanan siber", false], ["Penerbitan sertifikat akreditasi KAN", false]] }
                ]
            },
            {
                id: 4,
                name: "ICCOSH (Indonesian Conference & Competition OSH) Yogyakarta",
                category: "PMSMT",
                teamMembers: ["Nopiyanti", "Yayan Sopyan", "Wahyu Sukmawati"],
                urgency: "Sedang",
                status: "In Progress",
                progress: 45,
                deadline: "22 Mei 2026",
                daysLeft: "H-12 Hari",
                pic: "Nopiyanti / Tim K3 & SMTI",
                description: "Keikutsertaan 3 gugus inovasi unggulan PT Pupuk Kujang dalam ajang Konferensi dan Kompetisi K3 Tingkat Nasional di Yogyakarta.",
                alertNote: "Peringatan Dokumen: 2 dari 3 gugus belum mengumpulkan biodata lengkap dan surat pernyataan orisinalitas!",
                comments: [
                    { id: 1, author: "Nopiyanti", role: "Officer PMSMT", time: "16 Sep 2026, 11:30 WIB", text: "Surat peringatan pengumpulan berkas sudah dikirimkan ke fasilitator gugus 2 dan 3." }
                ],
                flow: [
                    { stepNumber: 1, title: "Izin Prinsip Direksi", date: "10 Apr 2026", status: "completed", desc: "Penerbitan memo izin prinsip keikutsertaan delegasi nomor 0387/C/SM/01400/MC/2026.", tasks: [["Persetujuan Direktur SDM & Umum", true], ["Alokasi anggaran pendaftaran", true]] },
                    { stepNumber: 2, title: "Penetapan 3 Gugus PKC", date: "18 Apr 2026", status: "completed", desc: "Seleksi internal dan penetapan 3 gugus terbaik sebagai perwakilan Pupuk Kujang.", tasks: [["SK penunjukan delegasi resmi", true], ["Penetapan pembina masing-masing gugus", true]] },
                    { stepNumber: 3, title: "Kelengkapan Dokumen & Makalah", date: "25 Apr - 12 Mei 2026", status: "active", desc: "Pengumpulan naskah makalah inovasi, poster K3, dan administrasi panitia ICCOSH.", tasks: [["Makalah Gugus 1 selesai", true], ["Makalah Gugus 2 & 3 revisi", false], ["Kelengkapan biodata peserta", false]] },
                    { stepNumber: 4, title: "Coaching & Simulasi", date: "13-16 Mei 2026", status: "pending", desc: "Latihan pemaparan materi di depan manajemen untuk pematangan presentasi.", tasks: [["Dry-run presentasi 15 menit", false], ["Pembuatan alat peraga / demo mockup", false]] },
                    { stepNumber: 5, title: "Pelaksanaan Kompetisi Yogya", date: "19-22 Mei 2026", status: "pending", desc: "Tanding di forum kompetisi K3 nasional di Yogyakarta dan penganugerahan award.", tasks: [["Presentasi di hadapan dewan juri", false], ["Pameran booth inovasi K3", false]] }
                ]
            },
            {
                id: 5,
                name: "Pengelolaan & Pendaftaran Paten Inovasi (Plantastic & TJSL)",
                category: "MIKU",
                teamMembers: ["Ari Citra Hermawan", "Putri Yunikeu"],
                urgency: "Sedang",
                status: "In Progress",
                progress: 70,
                deadline: "15 Juni 2026",
                daysLeft: "H-25 Hari",
                pic: "Ari Citra Hermawan / Inventor SMTI",
                description: "Proses pendaftaran hak paten resmi ke DJKI Kemenkumham untuk 2 judul inovasi: Plantastic 5 (Chatbot AI) dan Sistem Pencegahan Potensi Kebakaran TJSL.",
                alertNote: "Status Terkini: Dokumen kelengkapan revisi selesai diasistensikan, sedang proses pengusulan tambahan 2 inventor paten TJSL.",
                comments: [
                    { id: 1, author: "Ari Citra", role: "Officer HAKI", time: "16 Sep 2026, 12:00 WIB", text: "Asistensi DJKI menyarankan penajaman klaim metode deteksi pada sistem TJSL." }
                ],
                flow: [
                    { stepNumber: 1, title: "Drafting Deskripsi Paten", date: "5 Apr 2026", status: "completed", desc: "Penyusunan klaim paten, abstrak, gambar teknik, dan latar belakang inovasi.", tasks: [["Draft deskripsi Plantastic selesai", true], ["Draft deskripsi TJSL selesai", true]] },
                    { stepNumber: 2, title: "Asistensi Pakar Paten", date: "17 Apr 2026", status: "completed", desc: "Asistensi pendampingan bersama konsultan HAKI untuk uji kebaruan (novelty).", tasks: [["Hasil catatan asistensi diterima", true], ["Penyelarasan redaksional klaim", true]] },
                    { stepNumber: 3, title: "Revisi & Penambahan Inventor", date: "25 Apr - 20 Mei 2026", status: "active", desc: "Pengesahan surat kuasa inventor dan pengusulan penambahan 2 orang tim inventor TJSL.", tasks: [["Revisi berkas deskripsi final", true], ["Surat persetujuan penambahan inventor", false], ["Tanda tangan surat pernyataan kepemilikan", false]] },
                    { stepNumber: 4, title: "Submisi Online DJKI", date: "25 Mei 2026", status: "pending", desc: "Pendaftaran resmi melalui portal e-Paten Kemenkumham dan pembayaran PNBP.", tasks: [["Upload berkas dan gambar", false], ["Penerbitan Nomor Permohonan Paten", false]] },
                    { stepNumber: 5, title: "Pemeriksaan Substantif", date: "Juni 2026", status: "pending", desc: "Masa pengumuman publik dan pemeriksaan substantif pemeriksa paten DJKI.", tasks: [["Monitoring publikasi resmi", false], ["Penerbitan sertifikat paten", false]] }
                ]
            },
            {
                id: 6,
                name: "CIAS (Corporate Innovation Asia) - Training EBITDA Inovator",
                category: "MIKU",
                teamMembers: ["Mochamad Januardi", "Septian", "Yunni Kusriwanti"],
                urgency: "Sedang",
                status: "Planning",
                progress: 35,
                deadline: "30 Juni 2026",
                daysLeft: "H-40 Hari",
                pic: "Mochamad Januardi / HRD & SMTI",
                description: "Program training 4 sesi pembekalan inovator PKC fokus pada penyusunan proposal terstruktur dan validasi perhitungan EBITDA inovasi.",
                alertNote: "Menunggu konfirmasi jadwal training agar tidak bentrok dengan jadwal shift operasi pabrik.",
                comments: [],
                flow: [
                    { stepNumber: 1, title: "Penyusunan Proposal CIAS", date: "17 Apr 2026", status: "completed", desc: "Penyusunan kurikulum pelatihan 4 sesi (Understanding Process, Structuring, EBITDA, Sharing).", tasks: [["Silabus materi pelatihan disetujui", true], ["Kebutuhan kuota 30 peserta", true]] },
                    { stepNumber: 2, title: "Koordinasi Jadwal & Kuota", date: "2-20 Mei 2026", status: "active", desc: "Penyelarasan jadwal dengan unit kerja inovator agar kehadiran optimal.", tasks: [["Konfirmasi ketersediaan instruktur CIAS", true], ["Distribusi kuota per kompartemen", false]] },
                    { stepNumber: 3, title: "Penerbitan Surat Tugas", date: "25 Mei 2026", status: "pending", desc: "Penerbitan surat tugas resmi bagi 30 inovator terpilih.", tasks: [["Penerbitan ST dari SDM", false], ["Pra-tugas perhitungan awal", false]] },
                    { stepNumber: 4, title: "Pelaksanaan 4 Sesi Training", date: "Juni 2026", status: "pending", desc: "Pelaksanaan kelas interaktif dan bimbingan langsung perhitungan EBITDA.", tasks: [["Sesi 1 & 2: Konsep & Proposal", false], ["Sesi 3 & 4: EBITDA & Pitching", false]] },
                    { stepNumber: 5, title: "Evaluasi & Proposal Tervalidasi", date: "30 Juni 2026", status: "pending", desc: "Penyerahan proposal inovasi yang telah dilengkapi business case EBITDA valid.", tasks: [["Evaluasi hasil belajar", false], ["Sertifikat kelulusan peserta", false]] }
                ]
            },
            {
                id: 7,
                name: "Sosialisasi & Penilaian 5R Seluruh Unit Kerja",
                category: "PMSMT",
                teamMembers: ["Yayan Sopyan", "Nopiyanti"],
                urgency: "Rendah",
                status: "In Progress",
                progress: 50,
                deadline: "31 Agustus 2026",
                daysLeft: "On Track",
                pic: "Yayan Sopyan / Tim 5R",
                description: "Program rutin pembudayaan Ringkas, Rapi, Resik, Rawat, Rajin (5R) mencakup area pabrik, kantor administrasi, dan lingkungan perumahan dinas.",
                alertNote: "Jadwal: Sosialisasi Minggu 1-3 Agustus, dilanjutkan Penilaian Lapangan Minggu ke-4 Agustus 2026.",
                comments: [],
                flow: [
                    { stepNumber: 1, title: "Penerbitan IK 5R (PK-DPU-IK-0003)", date: "30 Juli 2026", status: "completed", desc: "Penerbitan Instruksi Kerja Penerapan 5R di Lingkungan Jasa Sipil Kawasan & Perumahan.", tasks: [["IK resmi bernomor disahkan", true], ["Sosialisasi dokumen ke pengawas", true]] },
                    { stepNumber: 2, title: "Sosialisasi 5R ke Unit Kerja", date: "1-21 Ags 2026", status: "active", desc: "Kunjungan sosialisasi standar 5R ke unit-unit kerja pabrik dan perkantoran.", tasks: [["Sosialisasi 8 unit kerja pabrik", true], ["Sosialisasi unit kerja non-pabrik", false]] },
                    { stepNumber: 3, title: "Pembersihan Serentak", date: "22-25 Ags 2026", status: "pending", desc: "Aksi bersih dan penataan mandiri oleh tiap unit kerja.", tasks: [["Pilah barang tak terpakai", false], ["Penandaan garis batas & label", false]] },
                    { stepNumber: 4, title: "Penilaian Lapangan Juri", date: "26-30 Ags 2026", status: "pending", desc: "Audit penilaian 5R langsung oleh tim juri gabungan SMTI.", tasks: [["Scoring checklist 5R lapangan", false], ["Dokumentasi before & after", false]] },
                    { stepNumber: 5, title: "Rapor & Awarding 5R", date: "31 Ags 2026", status: "pending", desc: "Pengumuman pemenang bendera 5R dan pemberian apresiasi kinerja unit terbersih.", tasks: [["Penerbitan rapor 5R triwulan", false], ["Penyerahan bendera emas & hitam", false]] }
                ]
            },
            {
                id: 8,
                name: "Pengurusan SNI Mitra Binaan & Rapat Single Branding PI",
                category: "Pengembangan Sistem dan Prosedur",
                teamMembers: ["Putri Yunikeu", "Wahyu Sukmawati"],
                urgency: "Rendah",
                status: "In Progress",
                progress: 40,
                deadline: "31 Agustus 2026",
                daysLeft: "On Track",
                pic: "Putri Yunikeu / Tim Standardisasi",
                description: "Pendampingan sertifikasi SNI produk mitra binaan UMKM serta harmonisasi regulasi SNI Single Branding bersama Holding Pupuk Indonesia.",
                alertNote: "Rapat koordinasi bersama holding PI diagendakan pada 11 Agustus 2026.",
                comments: [],
                flow: [
                    { stepNumber: 1, title: "Identifikasi Mitra Binaan", date: "25 Juli 2026", status: "completed", desc: "Pemetaan produk unggulan mitra binaan TJSL yang memenuhi kualifikasi SNI.", tasks: [["Data profil 5 mitra binaan", true], ["Uji kelayakan dokumen usaha", true]] },
                    { stepNumber: 2, title: "Rapat Single Branding PI", date: "11 Ags 2026", status: "active", desc: "Rapat penyelarasan standar penjenamaan logo SNI bersama holding Pupuk Indonesia.", tasks: [["Partisipasi dalam forum holding", true], ["Harmonisasi pedoman kemasan", false]] },
                    { stepNumber: 3, title: "Uji Laboratorium Sampel", date: "15-24 Ags 2026", status: "pending", desc: "Pengujian parameter mutu di laboratorium terakreditasi ISO 17025.", tasks: [["Pengambilan sampel uji", false], ["Hasil uji parameter mutu", false]] },
                    { stepNumber: 4, title: "Audit Lapangan LSPro", date: "25-29 Ags 2026", status: "pending", desc: "Audit kepatuhan proses produksi oleh Lembaga Sertifikasi Produk.", tasks: [["Verifikasi sanitasi & higienitas", false], ["Tindakan perbaikan bila ada", false]] },
                    { stepNumber: 5, title: "Penerbitan Sertifikat SNI", date: "31 Ags 2026", status: "pending", desc: "Penyerahan sertifikat SNI resmi kepada mitra binaan.", tasks: [["Sertifikat SPPT-SNI terbit", false], ["Izin pencantuman tanda SNI", false]] }
                ]
            },
            {
                id: 9,
                name: "Sertifikasi ISO 9001:2015 & ISO 14001 Audit Eksternal Surveilans 1 (TUV Rheinland)",
                category: "PMSMT",
                teamMembers: ["Dion Ridwan Giartomi", "Wahyu Sukmawati", "Henisya Permata Sari"],
                urgency: "Rendah",
                status: "Completed",
                progress: 100,
                deadline: "10 April 2026",
                daysLeft: "Selesai",
                pic: "Dion Ridwan Giartomi / Tim PMSMT",
                description: "Pelaksanaan audit surveillance eksternal sistem manajemen mutu dan lingkungan bersama auditor independen TUV Rheinland Indonesia.",
                alertNote: "Audit surveillance 1 selesai 100% tuntas dengan rekomendasi perpanjangan sertifikasi tanpa temuan Mayor!",
                comments: [
                    { id: 1, author: "Dion Ridwan Giartomi", role: "Officer Audit", time: "10 Apr 2026, 16:30 WIB", text: "Alhamdulillah audit surveillance 1 telah ditutup resmi (Closing Meeting) dengan hasil memuaskan dan tanpa temuan major." },
                    { id: 2, author: "Henisya Permata Sari", role: "VP SMTI", time: "11 Apr 2026, 08:30 WIB", text: "Terima kasih kepada seluruh tim perwakilan unit kerja atas dedikasi dan kesiapan dokumen audit." }
                ],
                flow: [
                    { stepNumber: 1, title: "Review Dokumen & Pre-Audit", date: "15-20 Mar 2026", status: "completed", desc: "Pemeriksaan kesiapan manual mutu, IK, dan prosedur operasional standar.", tasks: [["Verifikasi 42 manual dan IK operasional", true], ["Penyelarasan target KPI lingkungan", true]] },
                    { stepNumber: 2, title: "Opening Meeting Auditor Eksternal", date: "25 Mar 2026", status: "completed", desc: "Pertemuan pembukaan audit bersama tim auditor TUV Rheinland dan jajaran manajemen.", tasks: [["Pemaparan ruang lingkup audit", true], ["Konfirmasi jadwal visit pabrik & utilitas", true]] },
                    { stepNumber: 3, title: "Audit Lapangan Pabrik & Lab", date: "26-28 Mar 2026", status: "completed", desc: "Pemeriksaan kepatuhan proses produksi Pabrik 1A, 1B, NPK, dan laboratorium kendali mutu.", tasks: [["Sampling parameter limbah & emisi", true], ["Uji kepatuhan kalibrasi instrumen", true], ["Wawancara operator dan supervisor", true]] },
                    { stepNumber: 4, title: "Closing Meeting & Klarifikasi", date: "30 Mar 2026", status: "completed", desc: "Penyampaian resume audit dan klarifikasi catatan minor pemenuhan standar.", tasks: [["Pemaparan hasil temuan minor", true], ["Penyusunan matriks tindak lanjut CAR", true]] },
                    { stepNumber: 5, title: "Penerbitan Rekomendasi Sertifikat", date: "10 Apr 2026", status: "completed", desc: "Penyerahan laporan resmi audit surveillance dan rekomendasi kelanjutan sertifikasi.", tasks: [["Laporan resmi surveillance disetujui", true], ["Sertifikat surveilans 1 diserahkan", true]] }
                ]
            },
            {
                id: 10,
                name: "Implementasi & Sosialisasi Budaya 5R Terpadu Gudang & Kantor SMTI",
                category: "Pengembangan Sistem dan Prosedur",
                teamMembers: ["Yayan Sopyan", "Nopiyanti", "Ari Citra Hermawan"],
                urgency: "Rendah",
                status: "Completed",
                progress: 100,
                deadline: "25 Maret 2026",
                daysLeft: "Selesai",
                pic: "Yayan Sopyan / Tim 5R",
                description: "Program standardisasi penataan tempat kerja Ringkas, Rapi, Resik, Rawat, Rajin (5R), zonasi gudang suku cadang, dan sertifikasi kepatuhan 5R lingkungan SMTI.",
                alertNote: "Penilaian 5R batch 1 selesai dengan predikat Kategori Emas (Skor 94.2) dari Tim Penilai Pusat!",
                comments: [
                    { id: 1, author: "Yayan Sopyan", role: "Tim 5R SMTI", time: "25 Mar 2026, 14:15 WIB", text: "Seluruh zonasi penempatan dokumen dan suku cadang telah distandarisasi dengan visual management warna standar." },
                    { id: 2, author: "Nopiyanti", role: "Officer PMSMT", time: "25 Mar 2026, 15:45 WIB", text: "Sertifikat penghargaan 5R predikat Emas telah diterima dari Tim Manajemen Mutu." }
                ],
                flow: [
                    { stepNumber: 1, title: "Pemetaan Area & Zonasi Label", date: "1-5 Mar 2026", status: "completed", desc: "Penentuan batas area kerja, penomoran rak arsip, dan layout visual gudang.", tasks: [["Layout denah 5R disahkan", true], ["Pemasangan line pembatas lantai", true]] },
                    { stepNumber: 2, title: "Aksi Ringkas (Red Tag Campaign)", date: "6-10 Mar 2026", status: "completed", desc: "Penyortiran barang yang tidak diperlukan dan pemindahan ke area transit sortir.", tasks: [["Pemberian label merah barang afkir", true], ["Pemusnahan berkas kadaluarsa sesuai izin", true]] },
                    { stepNumber: 3, title: "Aksi Rapi & Resik Terpadu", date: "11-18 Mar 2026", status: "completed", desc: "Penataan alat kerja sesuai frekuensi penggunaan dan pembersihan menyeluruh.", tasks: [["Labeling identitas ordner & laci", true], ["Jadwal piket harian pembersihan", true]] },
                    { stepNumber: 4, title: "Audit Penilaian Mandiri (Rawat)", date: "19-22 Mar 2026", status: "completed", desc: "Pelaksanaan audit internal 5R berkala untuk memastikan standar tetap terpelihara.", tasks: [["Scoring checklist 5R mandiri", true], ["Dokumentasi foto before & after", true]] },
                    { stepNumber: 5, title: "Awarding & Sertifikasi 5R (Rajin)", date: "25 Mar 2026", status: "completed", desc: "Evaluasi dewan penilai dan penganugerahan predikat kepatuhan budaya 5R Emas.", tasks: [["Penilaian juri independen SMTI", true], ["Penganugerahan predikat Emas", true]] }
                ]
            }
        ];

        // Load persisted data or default with Vercel Cloud Storage Sync
        let projectDataSMTI = [];
        const VERCEL_API_ENDPOINT = (window.location.hostname.includes('localhost') || window.location.hostname.includes('127.0.0.1'))
            ? 'https://smti-pupuk-kujang.vercel.app/api/projects'
            : '/api/projects';

        let isSyncingToCloud = false;

        function updateCloudSyncBadge(status) {
            const badge = document.getElementById('cloud-sync-badge');
            if (!badge) return;

            if (status === 'syncing') {
                badge.className = 'cloud-sync-badge syncing';
                badge.innerHTML = '<i class="fas fa-sync fa-spin"></i> <span id="cloud-sync-text">Menyimpan ke Vercel...</span>';
            } else if (status === 'error') {
                badge.className = 'cloud-sync-badge error';
                badge.innerHTML = '<i class="fas fa-exclamation-triangle"></i> <span id="cloud-sync-text">Offline / Gagal Sync</span>';
                badge.title = 'Gagal terhubung ke Vercel Storage. Klik untuk mencoba lagi.';
            } else {
                badge.className = 'cloud-sync-badge';
                badge.innerHTML = '<i class="fas fa-cloud"></i> <span id="cloud-sync-text">Vercel Terhubung</span>';
                badge.title = 'Data tersimpan aman di Vercel Cloud Storage. Klik untuk menyegarkan data.';
            }
        }

        async function syncFromCloud(showNotification = false) {
            try {
                // Tarik data karyawan dan anak magang terbaru dari cloud
                fetchEmployeesFromCloud();
                fetchInternsFromCloud();
                const res = await fetch(VERCEL_API_ENDPOINT);
                if (res.ok) {
                    const json = await res.json();
                    if (json && json.success && Array.isArray(json.data) && json.data.length > 0) {
                        projectDataSMTI = json.data;
                        // Pastikan proyek selesai default ada jika belum pernah tersimpan di cloud
                        defaultProjectDataSMTI.forEach(defProj => {
                            if (!projectDataSMTI.some(p => p.id === defProj.id || p.name === defProj.name)) {
                                projectDataSMTI.push(JSON.parse(JSON.stringify(defProj)));
                            }
                        });
                        localStorage.setItem('smti_projects_data_v2', JSON.stringify(projectDataSMTI));
                        renderProjectsList();
                        renderMonitorBoard();
                        if (document.getElementById('flowModal') && document.getElementById('flowModal').classList.contains('active')) {
                            openFlowModal(currentActiveProjectId);
                        }
                        updateCloudSyncBadge('synced');
                        if (showNotification) {
                            alert("Data berhasil disinkronisasi langsung dari Vercel Cloud Storage!");
                        }
                        return;
                    }
                }
                updateCloudSyncBadge('synced');
            } catch (e) {
                console.log('Sync from cloud error:', e);
                updateCloudSyncBadge('error');
            }
        }

        async function syncToCloud() {
            if (isSyncingToCloud) return;
            isSyncingToCloud = true;
            updateCloudSyncBadge('syncing');
            try {
                const res = await fetch(VERCEL_API_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(projectDataSMTI)
                });
                if (res.ok) {
                    updateCloudSyncBadge('synced');
                } else {
                    updateCloudSyncBadge('error');
                }
            } catch (e) {
                console.log('Sync to cloud error:', e);
                updateCloudSyncBadge('error');
            } finally {
                isSyncingToCloud = false;
            }
        }

        function loadProjectsData() {
            try {
                const stored = localStorage.getItem('smti_projects_data_v2');
                if (stored) {
                    projectDataSMTI = JSON.parse(stored);
                } else {
                    projectDataSMTI = JSON.parse(JSON.stringify(defaultProjectDataSMTI));
                }
            } catch (e) {
                console.error("Gagal membaca localStorage, menggunakan default:", e);
                projectDataSMTI = JSON.parse(JSON.stringify(defaultProjectDataSMTI));
            }

            // Pastikan proyek default (termasuk proyek selesai 9 & 10) terintegrasi jika belum ada
            defaultProjectDataSMTI.forEach(defProj => {
                if (!projectDataSMTI.some(p => p.id === defProj.id || p.name === defProj.name)) {
                    projectDataSMTI.push(JSON.parse(JSON.stringify(defProj)));
                }
            });
        }

        function saveProjectsData() {
            try {
                localStorage.setItem('smti_projects_data_v2', JSON.stringify(projectDataSMTI));
            } catch (e) {
                console.error("Gagal menyimpan ke localStorage:", e);
            }

            // Otomatis sinkronisasi ke Vercel Cloud Storage (debounced 700ms)
            clearTimeout(window.syncCloudTimeout);
            window.syncCloudTimeout = setTimeout(syncToCloud, 700);
        }

        function resetToDefaultData() {
            if (confirm("Reset semua perubahan data checklist, progres, komentar, dan daftar karyawan ke kondisi awal?")) {
                localStorage.removeItem('smti_projects_data_v2');
                localStorage.removeItem('smti_employees_data_v2');
                projectDataSMTI = JSON.parse(JSON.stringify(defaultProjectDataSMTI));
                SMTI_EMPLOYEES = JSON.parse(JSON.stringify(defaultSMTIEmployees));
                saveEmployeesData();
                renderProjectsList();
                renderMonitorBoard();
                if (document.getElementById('flowModal').classList.contains('active')) {
                    openFlowModal(currentActiveProjectId);
                }
                saveProjectsData();
                alert("Data berhasil di-reset ke bawaan sistem dan disinkronkan ke Vercel Cloud.");
            }
        }

        let currentActiveProjectId = 1;
        let currentSelectedStepIndex = 2; // Default ke active step KIX
        let currentProjectFilter = "semua";
        let analyticsChartInstance = null;

        window.onload = function() {
            loadEmployeesData();
            fetchEmployeesFromCloud();
            loadInternsData();
            fetchInternsFromCloud();
            loadProjectsData();
            updateTotalCount();
            startClock();
            renderProjectsList();
            renderMonitorBoard();
            initMainDashboardChart();

            // Inisialisasi Sistem PIN & Auto-login di browser
            initAuthPinSystem();

            // Background fetch from Vercel Cloud Storage
            syncFromCloud();

            // Auto-polling data dari cloud setiap 20 detik (agar layar monitor TV & HP rekan ter-update otomatis)
            setInterval(syncFromCloud, 20000);
        };

        function startClock() {
            const updateTime = () => {
                const now = new Date();
                const timeString = now.toLocaleTimeString('id-ID') + ' WIB';
                const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                const dateString = now.toLocaleDateString('id-ID', options);

                const liveClock = document.getElementById('live-clock');
                if (liveClock) liveClock.innerText = timeString;

                const monClock = document.getElementById('monitor-live-clock');
                if (monClock) monClock.innerText = timeString;

                const monDate = document.getElementById('monitor-live-date');
                if (monDate) monDate.innerText = dateString;
            };
            updateTime();
            setInterval(updateTime, 1000);
        }

        /* --- CHART JS DASHBOARD --- */
        function initMainDashboardChart() {
            const ctx = document.getElementById('mainChart');
            if(!ctx) return;
            new Chart(ctx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'],
                    datasets: [{
                        label: 'Realisasi Inovasi & Tugas SMTI (%)',
                        data: [65, 70, 78, 92, 85, 80, 95],
                        borderColor: '#0284c7',
                        backgroundColor: 'rgba(2, 132, 199, 0.12)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.35,
                        pointBackgroundColor: '#0284c7'
                    }]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        }

        function initAnalyticsChart() {
            if(analyticsChartInstance) return;
            const ctx2 = document.getElementById('analyticsChart');
            if(!ctx2) return;
            analyticsChartInstance = new Chart(ctx2.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: ['KIX Inovasi', 'Digitalisasi', 'Audit SMT', 'Paten HAKI', 'CIAS EBITDA', '5R Kawasan'],
                    datasets: [{
                        label: 'Progres Penyelesaian (%)',
                        data: [27, 65, 80, 70, 35, 50],
                        backgroundColor: ['#dc2626', '#dc2626', '#dc2626', '#d97706', '#d97706', '#16a34a'],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true, max: 100 } }
                }
            });
        }

        /* --- NAVIGATION --- */
        function isCurrentUserSuperAdmin() {
            if (!currentAuthUser) return false;
            return !!(currentAuthUser.isSuperAdmin || (currentAuthUser.name && currentAuthUser.name.toLowerCase().includes('septian')));
        }

        function showPage(pageId, element) {
            const restrictedPages = ['karyawan', 'magang', 'pengaturan'];
            if (restrictedPages.includes(pageId) && !isCurrentUserSuperAdmin()) {
                alert("Akses Terbatas: Menu ini dikhususkan untuk Super Admin (Septian).");
                return;
            }

            document.querySelectorAll('.page-section').forEach(p => p.classList.remove('active'));
            const target = document.getElementById(pageId);
            if (target) target.classList.add('active');

            if(element) {
                document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
                element.classList.add('active');
            }

            const titles = { 
                dasbor: "Ringkasan Performa SMTI", 
                karyawan: "Manajemen Karyawan Dept SMTI", 
                magang: "Data Mahasiswa & Siswa Magang / PKL",
                proyek: "Status Proyek Berjalan & Alur Kerja",
                laporan: "Laporan & Analytics Departemen",
                pengaturan: "Pengaturan Sistem",
                bantuan: "Pusat Bantuan & Panduan"
            };
            document.getElementById('current-title').innerText = titles[pageId] || "Dashboard SMTI";

            if(pageId === 'karyawan') backToList();
            if(pageId === 'magang') { renderInternsTable(); updateInternsCount(); }
            if(pageId === 'proyek') renderProjectsList();
            if(pageId === 'laporan') setTimeout(initAnalyticsChart, 150);
        }

        /* =========================================================
           RENDER LIST PROYEK DI PAGE PROYEK (BERJALAN & SELESAI)
           ========================================================= */
        function isProjectCompleted(p) {
            return (p.status === 'Completed' || p.status === 'Finished' || p.progress >= 100);
        }

        function renderProjectsList() {
            const container = document.getElementById('project-card-container');
            if (!container) return;

            const filtered = projectDataSMTI.filter(p => {
                const done = isProjectCompleted(p);
                let matchFilter = true;
                if (currentProjectFilter === "semua") {
                    matchFilter = true;
                } else if (currentProjectFilter === "running" || currentProjectFilter === "berjalan") {
                    matchFilter = !done;
                } else if (currentProjectFilter === "selesai" || currentProjectFilter === "completed" || currentProjectFilter === "Finished") {
                    matchFilter = done;
                } else {
                    // Filter by urgency ("Tinggi", "Sedang", "Rendah")
                    matchFilter = p.urgency.toLowerCase() === currentProjectFilter.toLowerCase();
                }

                const matchCategory = currentCategoryFilter === "semua" || p.category === currentCategoryFilter;
                return matchFilter && matchCategory;
            });

            // Update KPI counts
            const totalCount = projectDataSMTI.length;
            const completedCount = projectDataSMTI.filter(p => isProjectCompleted(p)).length;
            const runningCount = totalCount - completedCount;
            const highCount = projectDataSMTI.filter(p => p.urgency === 'Tinggi').length;
            const medCount = projectDataSMTI.filter(p => p.urgency === 'Sedang').length;
            const lowCount = projectDataSMTI.filter(p => p.urgency === 'Rendah').length;

            if (document.getElementById('proyek-kpi-total')) document.getElementById('proyek-kpi-total').innerText = totalCount;
            if (document.getElementById('proyek-kpi-running')) document.getElementById('proyek-kpi-running').innerText = runningCount;
            if (document.getElementById('proyek-kpi-completed')) document.getElementById('proyek-kpi-completed').innerText = completedCount;
            if (document.getElementById('proyek-kpi-high')) document.getElementById('proyek-kpi-high').innerText = highCount;
            if (document.getElementById('proyek-kpi-med')) document.getElementById('proyek-kpi-med').innerText = medCount;
            if (document.getElementById('proyek-kpi-low')) document.getElementById('proyek-kpi-low').innerText = lowCount;

            // Update tab badge counters
            if (document.getElementById('count-proj-all')) document.getElementById('count-proj-all').innerText = totalCount;
            if (document.getElementById('count-proj-running')) document.getElementById('count-proj-running').innerText = runningCount;
            if (document.getElementById('count-proj-completed')) document.getElementById('count-proj-completed').innerText = completedCount;
            if (document.getElementById('count-proj-high')) document.getElementById('count-proj-high').innerText = highCount;
            if (document.getElementById('count-proj-med')) document.getElementById('count-proj-med').innerText = medCount;
            if (document.getElementById('count-proj-low')) document.getElementById('count-proj-low').innerText = lowCount;

            // Main Dashboard overview counts
            if (document.getElementById('dash-total-proyek')) document.getElementById('dash-total-proyek').innerText = totalCount;
            if (document.getElementById('dash-urgent-proyek')) document.getElementById('dash-urgent-proyek').innerText = highCount;
            if (document.getElementById('dash-med-proyek')) document.getElementById('dash-med-proyek').innerText = medCount;
            if (document.getElementById('side-urgent-count')) document.getElementById('side-urgent-count').innerText = highCount + " Urgent";

            if (filtered.length === 0) {
                container.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 40px 20px; opacity: 0.6;">
                        <i class="fas fa-search" style="font-size: 32px; margin-bottom: 10px; color: #94a3b8;"></i>
                        <p style="font-weight: 600; font-size: 14px;">Tidak ada proyek pada filter ini.</p>
                        <button class="btn btn-sm" style="margin-top: 8px; background: #0284c7;" onclick="filterProjects('semua', document.querySelector('.tab-btn[data-filter=\'semua\']'))">
                            Tampilkan Semua Proyek
                        </button>
                    </div>
                `;
                return;
            }

            container.innerHTML = filtered.map(p => {
                const done = isProjectCompleted(p);
                const urgencyClass = p.urgency === 'Tinggi' ? 'high' : (p.urgency === 'Sedang' ? 'med' : 'low');
                const cardClass = done ? 'card-status-completed' : (p.urgency === 'Tinggi' ? 'card-urgency-high' : (p.urgency === 'Sedang' ? 'card-urgency-med' : 'card-urgency-low'));
                const urgencyIcon = p.urgency === 'Tinggi' ? 'fa-fire' : (p.urgency === 'Sedang' ? 'fa-clock' : 'fa-check-circle');

                // Generate mini stepper nodes
                const miniStepsHtml = p.flow.map((st, i) => `
                    <div class="mini-step-node ${st.status}" title="Tahap ${st.stepNumber}: ${st.title} (${st.status})">
                        ${st.status === 'completed' ? '<i class="fas fa-check"></i>' : st.stepNumber}
                    </div>
                `).join('');

                const activeStep = done
                    ? { title: "Tuntas Selesai (100%)" }
                    : (p.flow.find(st => st.status === 'active') || p.flow[p.flow.length - 1]);

                return `
                    <div class="project-card-item ${cardClass}" onclick="openFlowModal(${p.id})">
                        <div>
                            <div class="project-card-top">
                                <span class="project-category-tag">${p.category}</span>
                                ${done ? `
                                    <span class="urgency-badge" style="background: rgba(22, 163, 74, 0.12); color: #16a34a; border: 1px solid rgba(22, 163, 74, 0.3);">
                                        <i class="fas fa-check-circle"></i> Selesai (100%)
                                    </span>
                                ` : `
                                    <span class="urgency-badge ${urgencyClass}">
                                        <i class="fas ${urgencyIcon}"></i> Urgensi ${p.urgency}
                                    </span>
                                `}
                            </div>

                            <h3 class="project-card-title">${p.name}</h3>
                            <p class="project-card-desc">${p.description}</p>

                            <!-- Mini Workflow Stepper -->
                            <div class="card-flow-preview">
                                <div class="card-flow-header">
                                    <span>Tahap: <strong style="color: ${done ? '#16a34a' : '#0284c7'};">${activeStep.title}</strong></span>
                                    <span><strong style="color: ${done ? '#16a34a' : 'inherit'};">${p.progress}%</strong></span>
                                </div>
                                <div class="mini-stepper">
                                    <div class="mini-stepper-line" style="${done ? 'background: #16a34a;' : ''}"></div>
                                    ${miniStepsHtml}
                                </div>
                            </div>

                            <!-- Team Avatars Stack Preview -->
                            ${(p.teamMembers && p.teamMembers.length > 0) ? `
                                <div style="display: flex; align-items: center; gap: 5px; margin-top: 10px; margin-bottom: 4px;">
                                    <span style="font-size: 11px; color: #64748b; font-weight: 700; margin-right: 4px;"><i class="fas fa-users"></i> Tim:</span>
                                    ${p.teamMembers.slice(0, 4).map(mName => {
                                        const emp = (window.SMTI_EMPLOYEES || []).find(e => e.name.toLowerCase() === mName.toLowerCase()) || 
                                                    (window.SMTI_INTERNS || []).find(i => i.name.toLowerCase() === mName.toLowerCase()) || 
                                                    { name: mName, initials: mName.substring(0,2).toUpperCase(), color: '#0284c7' };
                                        return `<div class="team-avatar-circle" style="background: ${emp.color || '#0284c7'}; width: 22px; height: 22px; font-size: 9.5px;" title="${mName}">${emp.initials || mName.substring(0,2).toUpperCase()}</div>`;
                                    }).join('')}
                                    ${p.teamMembers.length > 4 ? `<span style="font-size: 10.5px; color: #64748b; font-weight: 700; margin-left: 2px;">+${p.teamMembers.length - 4}</span>` : ''}
                                </div>
                            ` : ''}
                        </div>

                        <div>
                            <div class="project-card-meta">
                                <span><i class="fas fa-user-circle"></i> ${p.pic}</span>
                                ${done ? `
                                    <span class="project-deadline-pill" style="background: rgba(22, 163, 74, 0.12); color: #16a34a; font-weight: 700;">
                                        <i class="fas fa-flag-checkered"></i> Selesai (${p.deadline})
                                    </span>
                                ` : `
                                    <span class="project-deadline-pill"><i class="fas fa-calendar-alt"></i> ${p.deadline} (${p.daysLeft})</span>
                                `}
                            </div>

                            <button class="btn-view-flow" style="${done ? 'border-color: #16a34a; color: #16a34a; background: rgba(22, 163, 74, 0.05);' : ''}" onclick="event.stopPropagation(); openFlowModal(${p.id})">
                                <i class="fas ${done ? 'fa-check-circle' : 'fa-sitemap'}"></i> ${done ? 'Buka Arsip & Hasil Akhir' : 'Buka Flow & Detail Progres'}
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function filterProjects(filterVal, btn) {
            currentProjectFilter = filterVal;
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            if (btn) {
                btn.classList.add('active');
            } else {
                const targetBtn = document.querySelector(`.tab-btn[data-filter='${filterVal}']`);
                if (targetBtn) targetBtn.classList.add('active');
            }
            renderProjectsList();
        }

        function searchProjects(e) {
            const query = e.target.value.toLowerCase().trim();
            const cards = document.querySelectorAll('.project-card-item');
            cards.forEach(card => {
                const text = card.innerText.toLowerCase();
                card.style.display = text.includes(query) ? '' : 'none';
            });
        }

        /* =========================================================
           RENDER MODE LAYAR MONITOR TV (PENGINGAT DEADLINE & FILTER)
           ========================================================= */
        let currentMonitorUrgencyFilter = 'semua';
        let currentMonitorCategoryFilter = 'semua';

        function openMonitorMode() {
            document.getElementById('monitor-overlay').classList.add('active');
            renderMonitorBoard();
        }

        function closeMonitorMode() {
            document.getElementById('monitor-overlay').classList.remove('active');
            if (document.fullscreenElement) {
                document.exitFullscreen().catch(() => {});
            }
        }

        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    alert("Gagal mengaktifkan mode fullscreen: " + err.message);
                });
            } else {
                document.exitFullscreen().catch(() => {});
            }
        }

        function setMonitorUrgencyFilter(filterVal, btnEl) {
            currentMonitorUrgencyFilter = filterVal;
            document.querySelectorAll('.mon-pill-btn').forEach(btn => btn.classList.remove('active'));
            if (btnEl) {
                btnEl.classList.add('active');
            } else {
                const mapId = { 'semua': 'mon-btn-all', 'Tinggi': 'mon-btn-high', 'Sedang': 'mon-btn-med', 'Rendah': 'mon-btn-low' };
                const target = document.getElementById(mapId[filterVal]);
                if (target) target.classList.add('active');
            }
            renderMonitorBoard();
        }

        function setMonitorCategoryFilter(catVal) {
            currentMonitorCategoryFilter = catVal;
            renderMonitorBoard();
        }

        function renderMonitorBoard() {
            const highList = document.getElementById('monitor-list-high');
            const medList = document.getElementById('monitor-list-med');
            const lowList = document.getElementById('monitor-list-low');
            const colHigh = document.getElementById('mon-col-high');
            const colMed = document.getElementById('mon-col-med');
            const colLow = document.getElementById('mon-col-low');
            const board = document.querySelector('.monitor-board');

            if (!highList || !medList || !lowList || !colHigh || !colMed || !colLow || !board) return;

            // Filter by category if set
            let filteredProjects = projectDataSMTI;
            if (currentMonitorCategoryFilter && currentMonitorCategoryFilter !== 'semua') {
                filteredProjects = filteredProjects.filter(p => p.category === currentMonitorCategoryFilter);
            }

            const highProjects = filteredProjects.filter(p => p.urgency === 'Tinggi');
            const medProjects = filteredProjects.filter(p => p.urgency === 'Sedang');
            const lowProjects = filteredProjects.filter(p => p.urgency === 'Rendah');

            // Update column badges
            document.getElementById('mon-count-high').innerText = highProjects.length + " Proyek";
            document.getElementById('mon-count-med').innerText = medProjects.length + " Proyek";
            document.getElementById('mon-count-low').innerText = lowProjects.length + " Proyek";

            // Update filter pill counters
            const pAll = document.getElementById('mon-pill-count-all');
            const pHigh = document.getElementById('mon-pill-count-high');
            const pMed = document.getElementById('mon-pill-count-med');
            const pLow = document.getElementById('mon-pill-count-low');
            if (pAll) pAll.innerText = filteredProjects.length;
            if (pHigh) pHigh.innerText = highProjects.length;
            if (pMed) pMed.innerText = medProjects.length;
            if (pLow) pLow.innerText = lowProjects.length;

            // Handle Column Visibility & Grid Expansion based on currentMonitorUrgencyFilter
            if (currentMonitorUrgencyFilter === 'Tinggi') {
                colHigh.style.display = 'flex';
                colMed.style.display = 'none';
                colLow.style.display = 'none';
                board.style.gridTemplateColumns = '1fr';
                highList.className = 'monitor-card-list monitor-card-list-expanded';
            } else if (currentMonitorUrgencyFilter === 'Sedang') {
                colHigh.style.display = 'none';
                colMed.style.display = 'flex';
                colLow.style.display = 'none';
                board.style.gridTemplateColumns = '1fr';
                medList.className = 'monitor-card-list monitor-card-list-expanded';
            } else if (currentMonitorUrgencyFilter === 'Rendah') {
                colHigh.style.display = 'none';
                colMed.style.display = 'none';
                colLow.style.display = 'flex';
                board.style.gridTemplateColumns = '1fr';
                lowList.className = 'monitor-card-list monitor-card-list-expanded';
            } else {
                colHigh.style.display = 'flex';
                colMed.style.display = 'flex';
                colLow.style.display = 'flex';
                board.style.gridTemplateColumns = 'repeat(3, 1fr)';
                highList.className = 'monitor-card-list';
                medList.className = 'monitor-card-list';
                lowList.className = 'monitor-card-list';
            }

            const createMonitorCard = (p, colorClass, barClass) => {
                const activeStep = p.flow.find(st => st.status === 'active') || p.flow[p.flow.length - 1];
                const daysColor = p.urgency === 'Tinggi' ? '#f87171' : (p.urgency === 'Sedang' ? '#fbbf24' : '#4ade80');
                return `
                    <div class="monitor-project-card ${colorClass}" onclick="openFlowModal(${p.id})">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                            <span style="font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">${p.category}</span>
                            <span style="font-size: 11px; font-weight: 800; color: ${daysColor};"><i class="fas fa-clock"></i> ${p.daysLeft}</span>
                        </div>
                        <div class="monitor-card-title">${p.name}</div>
                        <div class="monitor-card-stage">
                            <i class="fas fa-arrow-circle-right" style="color: #38bdf8;"></i> Tahap: <span class="monitor-stage-highlight">${activeStep.title}</span>
                        </div>

                        <div class="monitor-progress-box">
                            <div class="monitor-progress-label">
                                <span>Progres Kerja</span>
                                <strong>${p.progress}%</strong>
                            </div>
                            <div class="monitor-progress-track">
                                <div class="monitor-progress-bar ${barClass}" style="width: ${p.progress}%;"></div>
                            </div>
                        </div>

                        <div class="monitor-card-footer">
                            <span><i class="fas fa-user-circle"></i> ${p.pic}</span>
                            <span class="monitor-click-hint"><i class="fas fa-eye"></i> Klik Flow</span>
                        </div>
                    </div>
                `;
            };

            const emptyStateHtml = (urgencyName) => `
                <div style="text-align: center; padding: 45px 20px; color: #94a3b8; font-size: 13px; grid-column: 1 / -1; width: 100%; border: 1px dashed rgba(255,255,255,0.12); border-radius: 12px; margin: 10px 0;">
                    <i class="fas fa-folder-open" style="font-size: 32px; opacity: 0.4; margin-bottom: 10px; display: block;"></i>
                    Tidak ada proyek dengan status ${urgencyName} saat ini.
                </div>
            `;

            highList.innerHTML = highProjects.length > 0
                ? highProjects.map(p => createMonitorCard(p, 'monitor-card-high', 'bar-high')).join('')
                : emptyStateHtml('Urgensi Tinggi');

            medList.innerHTML = medProjects.length > 0
                ? medProjects.map(p => createMonitorCard(p, 'monitor-card-med', 'bar-med')).join('')
                : emptyStateHtml('Urgensi Sedang');

            lowList.innerHTML = lowProjects.length > 0
                ? lowProjects.map(p => createMonitorCard(p, 'monitor-card-low', 'bar-low')).join('')
                : emptyStateHtml('Rutin & Monitoring');
        }

        // Keyboard navigation for Monitor Mode (1: Semua, 2: Tinggi, 3: Sedang, 4: Rutin, Esc: Tutup)
        document.addEventListener('keydown', function(e) {
            const overlay = document.getElementById('monitor-overlay');
            if (!overlay || !overlay.classList.contains('active')) return;

            if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

            if (e.key === '1') {
                setMonitorUrgencyFilter('semua');
            } else if (e.key === '2') {
                setMonitorUrgencyFilter('Tinggi');
            } else if (e.key === '3') {
                setMonitorUrgencyFilter('Sedang');
            } else if (e.key === '4') {
                setMonitorUrgencyFilter('Rendah');
            } else if (e.key === 'Escape') {
                const flowModal = document.getElementById('flowModal');
                if (flowModal && flowModal.classList.contains('active')) {
                    closeFlowModal();
                } else {
                    closeMonitorMode();
                }
            }
        });

        /* =========================================================
           MODAL ALUR PROGRES INTERAKTIF (FLOW STEPPER MODAL)
           ========================================================= */
        function openFlowModal(projectId) {
            currentActiveProjectId = projectId;
            const project = projectDataSMTI.find(p => p.id === projectId);
            if (!project) return;

            document.getElementById('modal-project-title').innerText = project.name;
            document.getElementById('modal-project-desc').innerText = project.description;
            document.getElementById('modal-project-category').innerText = project.category;
            
            const urgencyBadge = document.getElementById('modal-project-urgency');
            urgencyBadge.innerText = 'Urgensi ' + project.urgency;
            urgencyBadge.className = 'urgency-badge ' + (project.urgency === 'Tinggi' ? 'high' : (project.urgency === 'Sedang' ? 'med' : 'low'));

            const isFinished = isProjectCompleted(project);
            const statusBadge = document.getElementById('modal-project-status');
            statusBadge.innerText = isFinished ? 'Sudah Selesai (100%)' : (project.status || 'In Progress');
            statusBadge.style.background = isFinished ? '#dcfce7' : 'rgba(2, 132, 199, 0.12)';
            statusBadge.style.color = isFinished ? '#166534' : '#0284c7';

            document.getElementById('modal-meta-deadline').innerText = `${project.deadline} (${project.daysLeft})`;
            document.getElementById('modal-meta-pic').innerText = project.pic;
            document.getElementById('modal-meta-progress').innerText = `${project.progress}% Selesai`;
            document.getElementById('manual-progress-input').value = project.progress;

            // Render Stepper Nodes
            renderModalStepper(project);

            // Default ke step yang active
            const activeIndex = project.flow.findIndex(st => st.status === 'active');
            selectModalStep(activeIndex !== -1 ? activeIndex : 0);

            // Render Tim Proyek & Author Select
            renderProjectTeam(project);
            populateChatAuthorSelect(project);

            // Render Comments / Progress Chat
            renderComments(project);

            document.getElementById('flowModal').classList.add('active');
        }

        function closeFlowModal() {
            document.getElementById('flowModal').classList.remove('active');
        }

        function renderModalStepper(project) {
            const stepperContainer = document.getElementById('modal-stepper-pipeline');
            if (!stepperContainer) return;

            stepperContainer.innerHTML = project.flow.map((st, index) => {
                const icon = st.status === 'completed' ? '<i class="fas fa-check"></i>' : (st.status === 'active' ? '<i class="fas fa-spinner fa-spin"></i>' : st.stepNumber);
                return `
                    <div class="step-item ${st.status}" onclick="selectModalStep(${index})" id="step-node-${index}">
                        <div class="step-circle">${icon}</div>
                        <div class="step-name">${st.title}</div>
                        <div class="step-date">${st.date}</div>
                    </div>
                `;
            }).join('');
        }

        function selectModalStep(index) {
            currentSelectedStepIndex = index;
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project || !project.flow[index]) return;

            const step = project.flow[index];

            // Highlight node visually
            document.querySelectorAll('.step-item').forEach((el, idx) => {
                if (idx === index) {
                    el.style.transform = 'scale(1.08)';
                } else {
                    el.style.transform = 'scale(1)';
                }
            });

            const badge = document.getElementById('modal-active-stage-badge');
            if (step.status === 'completed') {
                badge.innerText = `Tahap ${step.stepNumber} • Selesai (Completed)`;
                badge.className = 'stage-badge-current';
                badge.style.background = '#16a34a';
            } else if (step.status === 'active') {
                badge.innerText = `Tahap ${step.stepNumber} • Sedang Berjalan (Active)`;
                badge.className = project.urgency === 'Tinggi' ? 'stage-badge-urgent' : 'stage-badge-current';
                badge.style.background = project.urgency === 'Tinggi' ? '#dc2626' : '#0284c7';
            } else {
                badge.innerText = `Tahap ${step.stepNumber} • Menunggu (Pending)`;
                badge.className = 'stage-badge-current';
                badge.style.background = '#64748b';
            }

            document.getElementById('modal-active-stage-title').innerText = step.title;
            document.getElementById('modal-active-stage-date').innerText = step.date;
            document.getElementById('modal-active-stage-desc').innerText = step.desc;

            // Alert note
            const alertBox = document.getElementById('modal-stage-alert');
            const alertText = document.getElementById('modal-stage-alert-text');
            if (project.alertNote && (step.status === 'active' || project.urgency === 'Tinggi')) {
                alertText.innerText = project.alertNote;
                alertBox.style.display = 'flex';
            } else {
                alertBox.style.display = 'none';
            }

            // Render Checklist Tasks
            renderStageTasks(project, index);

            document.getElementById('modal-meta-stage').innerText = `Tahap ${step.stepNumber} dari ${project.flow.length}`;
        }

        /* =========================================================
           CHECKLIST KEGIATAN: RENDER, TOGGLE, INPUT MANUAL & DELETE
           ========================================================= */
        function renderStageTasks(project, stepIndex) {
            const step = project.flow[stepIndex];
            const checklistContainer = document.getElementById('modal-stage-checklist');
            const summaryText = document.getElementById('checklist-summary-text');
            if (!checklistContainer) return;

            const total = step.tasks ? step.tasks.length : 0;
            const completed = step.tasks ? step.tasks.filter(t => t[1]).length : 0;
            summaryText.innerText = `${completed}/${total} selesai`;

            if (!step.tasks || step.tasks.length === 0) {
                checklistContainer.innerHTML = `
                    <div style="padding: 12px; text-align: center; color: #94a3b8; font-size: 12.5px; border: 1px dashed var(--border-color); border-radius: 6px; margin-bottom: 8px;">
                        Belum ada tugas/dokumen syarat di tahap ini. Tambahkan di bawah.
                    </div>
                `;
                return;
            }

            checklistContainer.innerHTML = step.tasks.map((task, tIdx) => `
                <div class="task-item ${task[1] ? 'checked' : ''}" onclick="toggleTask(${stepIndex}, ${tIdx})">
                    <div class="task-left">
                        <input type="checkbox" ${task[1] ? 'checked' : ''} onclick="event.stopPropagation(); toggleTask(${stepIndex}, ${tIdx})">
                        <span>${task[0]}</span>
                    </div>
                    <button class="task-delete-btn" onclick="event.stopPropagation(); deleteTask(${stepIndex}, ${tIdx})" title="Hapus kegiatan ini">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            `).join('');
        }

        function toggleTask(stepIndex, taskIndex) {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project || !project.flow[stepIndex]) return;

            const isChecked = project.flow[stepIndex].tasks[taskIndex][1];
            project.flow[stepIndex].tasks[taskIndex][1] = !isChecked;

            recalculateAutoProgress(project);
            saveProjectsData();

            selectModalStep(stepIndex);
            renderProjectsList();
            renderMonitorBoard();
        }

        function addNewTask() {
            const input = document.getElementById('new-task-input');
            const taskText = input.value.trim();
            if (!taskText) {
                input.focus();
                return;
            }

            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project || !project.flow[currentSelectedStepIndex]) return;

            if (!project.flow[currentSelectedStepIndex].tasks) {
                project.flow[currentSelectedStepIndex].tasks = [];
            }

            // Push new task [taskName, false]
            project.flow[currentSelectedStepIndex].tasks.push([taskText, false]);
            input.value = "";

            recalculateAutoProgress(project);
            saveProjectsData();

            selectModalStep(currentSelectedStepIndex);
            renderProjectsList();
            renderMonitorBoard();
        }

        function deleteTask(stepIndex, taskIndex) {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project || !project.flow[stepIndex]) return;

            const taskName = project.flow[stepIndex].tasks[taskIndex][0];
            if (confirm(`Hapus checklist "${taskName}"?`)) {
                project.flow[stepIndex].tasks.splice(taskIndex, 1);
                recalculateAutoProgress(project);
                saveProjectsData();

                selectModalStep(stepIndex);
                renderProjectsList();
                renderMonitorBoard();
            }
        }

        function recalculateAutoProgress(project) {
            let totalTasks = 0;
            let completedTasks = 0;
            project.flow.forEach(st => {
                if (st.tasks) {
                    st.tasks.forEach(t => {
                        totalTasks++;
                        if (t[1]) completedTasks++;
                    });
                }
            });

            if (totalTasks > 0) {
                project.progress = Math.round((completedTasks / totalTasks) * 100);
            }

            document.getElementById('modal-meta-progress').innerText = `${project.progress}% Selesai`;
            document.getElementById('manual-progress-input').value = project.progress;
        }

        /* =========================================================
           KASUS PROGRES SUDAH SELESAI & KONTROL STATUS FLEKSIBEL
           ========================================================= */
        function setStepStatusManually(newStatus) {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project || !project.flow[currentSelectedStepIndex]) return;

            const currentStep = project.flow[currentSelectedStepIndex];
            currentStep.status = newStatus;

            // Jika diset completed, otomatis centang semua tugas di tahap ini
            if (newStatus === 'completed' && currentStep.tasks) {
                currentStep.tasks.forEach(t => t[1] = true);
            }

            // Update status keseluruhan proyek jika tahap terakhir selesai
            const allCompleted = project.flow.every(st => st.status === 'completed');
            if (allCompleted) {
                project.status = 'Finished';
                project.progress = 100;
            } else if (project.status === 'Finished') {
                project.status = 'In Progress';
            }

            recalculateAutoProgress(project);
            saveProjectsData();

            renderModalStepper(project);
            selectModalStep(currentSelectedStepIndex);
            renderProjectsList();
            renderMonitorBoard();
        }

        function applyManualProgress() {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;

            const val = parseInt(document.getElementById('manual-progress-input').value, 10);
            if (isNaN(val) || val < 0 || val > 100) {
                alert("Nilai progres harus antara 0 sampai 100 persen.");
                return;
            }

            project.progress = val;
            if (val === 100) {
                project.status = 'Finished';
                // Mark all steps as completed if user sets 100%
                project.flow.forEach(st => {
                    st.status = 'completed';
                    if (st.tasks) st.tasks.forEach(t => t[1] = true);
                });
            } else if (project.status === 'Finished' && val < 100) {
                project.status = 'In Progress';
            }

            saveProjectsData();
            document.getElementById('modal-meta-progress').innerText = `${project.progress}% Selesai`;
            renderModalStepper(project);
            selectModalStep(currentSelectedStepIndex);
            renderProjectsList();
            renderMonitorBoard();
            alert(`Progres proyek berhasil diatur ke ${val}%!`);
        }

        function advanceStage() {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;

            const currentIndex = project.flow.findIndex(st => st.status === 'active');
            if (currentIndex !== -1) {
                project.flow[currentIndex].status = 'completed';
                if (project.flow[currentIndex].tasks) {
                    project.flow[currentIndex].tasks.forEach(t => t[1] = true);
                }

                if (currentIndex + 1 < project.flow.length) {
                    project.flow[currentIndex + 1].status = 'active';
                    project.progress = Math.min(100, Math.round(((currentIndex + 1) / project.flow.length) * 100));
                } else {
                    project.status = 'Finished';
                    project.progress = 100;
                    alert(`Selamat! Seluruh tahapan proyek "${project.name}" telah selesai!`);
                }

                saveProjectsData();
                renderModalStepper(project);
                selectModalStep(Math.min(currentIndex + 1, project.flow.length - 1));
                renderProjectsList();
                renderMonitorBoard();
            }
        }

        function markProjectCompletedQuick() {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;
            
            if (confirm(`Tandai proyek "${project.name}" sebagai SELESAI (100%)?\nSeluruh tahapan dan checklist kegiatan akan ditandai tuntas.`)) {
                project.status = 'Completed';
                project.progress = 100;
                project.daysLeft = 'Selesai';
                project.flow.forEach(st => {
                    st.status = 'completed';
                    if (st.tasks) st.tasks.forEach(t => t[1] = true);
                });
                
                if (!project.comments) project.comments = [];
                const author = (document.getElementById('comment-author-select') && document.getElementById('comment-author-select').value) || 'Admin SMTI';
                const now = new Date();
                const timeStr = now.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' }) + ', ' + 
                                now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }) + ' WIB';
                project.comments.push({
                    id: Date.now(),
                    author: author,
                    role: "PIC / Admin SMTI",
                    time: timeStr,
                    tag: "done",
                    text: `✅ Proyek telah resmi ditandai selesai 100%. Seluruh tahapan kegiatan dan checklist verifikasi telah tuntas dilaksanakan.`
                });

                saveProjectsData();
                renderModalStepper(project);
                selectModalStep(project.flow.length - 1);
                renderCommentsList(project);
                renderProjectsList();
                renderMonitorBoard();
                alert(`Selamat! Proyek "${project.name}" berhasil ditandai selesai 100%!`);
            }
        }

        function reopenOrResetProject() {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;

            if (confirm(`Buka ulang (re-open) proyek "${project.name}" untuk revisi atau audit ulang?`)) {
                project.status = 'In Progress';
                // Set step 1 active, others pending
                project.flow.forEach((st, i) => {
                    st.status = i === 0 ? 'active' : 'pending';
                    if (st.tasks) st.tasks.forEach(t => t[1] = false);
                });
                project.progress = 10;
                saveProjectsData();

                renderModalStepper(project);
                selectModalStep(0);
                renderProjectsList();
                renderMonitorBoard();
                alert("Proyek telah dibuka kembali!");
            }
        }

        function editAlertNote() {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;

            const newNote = prompt("Ubah Catatan Urgensi / Status Terkini:", project.alertNote || "");
            if (newNote !== null) {
                project.alertNote = newNote.trim();
                saveProjectsData();
                selectModalStep(currentSelectedStepIndex);
                renderProjectsList();
            }
        }

        /* =========================================================
           MANAJEMEN TIM PROYEK, INVITE KARYAWAN & CHAT PROGRES
           ========================================================= */
        function renderProjectTeam(project) {
            const container = document.getElementById('modal-team-avatars-list');
            const countBadge = document.getElementById('modal-team-count');
            if (!container) return;

            if (!project.teamMembers) {
                project.teamMembers = [];
            }

            if (countBadge) countBadge.innerText = project.teamMembers.length;

            if (project.teamMembers.length === 0) {
                container.innerHTML = `
                    <span style="font-size: 12px; color: #94a3b8; font-style: italic;">
                        Belum ada karyawan ter-invite. Klik "+ Undang Karyawan SMTI" di samping.
                    </span>
                `;
                return;
            }

            container.innerHTML = project.teamMembers.map(name => {
                const isIntern = SMTI_INTERNS && SMTI_INTERNS.find(i => i.name.toLowerCase() === name.toLowerCase());
                const person = SMTI_EMPLOYEES.find(e => e.name.toLowerCase() === name.toLowerCase()) || isIntern || {
                    name: name,
                    role: "Anggota Tim",
                    initials: name.substring(0, 2).toUpperCase(),
                    color: "#0284c7"
                };
                const internBadge = isIntern ? ' <small style="color: #10b981; font-weight: 700; font-size: 10px;">(Magang)</small>' : '';
                return `
                    <div class="team-member-pill" title="${person.name} (${person.role}${isIntern ? ' • ' + isIntern.campus : ''})">
                        <div class="team-avatar-circle" style="background: ${person.color}; ${isIntern ? 'border: 2px solid #10b981;' : ''}">
                            ${person.initials}
                        </div>
                        <span>${person.name}${internBadge}</span>
                        <button type="button" class="team-member-remove" onclick="removeMemberFromProject('${person.name.replace(/'/g, "\\'")}')" title="Keluarkan dari tim proyek">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `;
            }).join('');
        }

        function openInviteTeamModal() {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;
            if (!project.teamMembers) project.teamMembers = [];

            const list = document.getElementById('invite-employees-list');
            if (!list) return;

            let html = `<div style="font-size: 11.5px; font-weight: 700; color: #0284c7; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;"><i class="fas fa-user-tie"></i> Karyawan SMTI:</div>`;
            html += SMTI_EMPLOYEES.map(emp => {
                const isInvited = project.teamMembers.some(m => m.toLowerCase() === emp.name.toLowerCase());
                return `
                    <div style="display: flex; justify-content: space-between; align-items: center; background: var(--hover-color); padding: 9px 12px; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 6px;">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div class="team-avatar-circle" style="background: ${emp.color}; width: 32px; height: 32px; font-size: 12px;">
                                ${emp.initials}
                            </div>
                            <div>
                                <strong style="font-size: 13px; color: var(--text-color);">${emp.name}</strong>
                                <div style="font-size: 11px; color: #64748b;">${emp.role}</div>
                            </div>
                        </div>
                        <div>
                            ${isInvited ? `
                                <button type="button" class="btn btn-sm" style="background: rgba(22, 163, 74, 0.15); color: #16a34a; border: 1px solid rgba(22, 163, 74, 0.3); font-weight: 700;" onclick="toggleInviteEmployee('${emp.name.replace(/'/g, "\\'")}')">
                                    <i class="fas fa-check"></i> Ter-invite
                                </button>
                            ` : `
                                <button type="button" class="btn btn-sm" style="background: #0284c7; font-weight: 700;" onclick="toggleInviteEmployee('${emp.name.replace(/'/g, "\\'")}')">
                                    <i class="fas fa-user-plus"></i> + Undang
                                </button>
                            `}
                        </div>
                    </div>
                `;
            }).join('');

            if (SMTI_INTERNS && SMTI_INTERNS.length > 0) {
                html += `<div style="font-size: 11.5px; font-weight: 700; color: #10b981; margin: 14px 0 6px 0; display: flex; align-items: center; gap: 6px;"><i class="fas fa-user-graduate"></i> Mahasiswa / Anak Magang SMTI:</div>`;
                html += SMTI_INTERNS.map(intern => {
                    const isInvited = project.teamMembers.some(m => m.toLowerCase() === intern.name.toLowerCase());
                    return `
                        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(16, 185, 129, 0.05); padding: 9px 12px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.25); margin-bottom: 6px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div class="team-avatar-circle" style="background: ${intern.color || '#10b981'}; width: 32px; height: 32px; font-size: 12px; border: 2px solid #10b981;">
                                    ${intern.initials || intern.name.slice(0, 2).toUpperCase()}
                                </div>
                                <div>
                                    <div style="display: flex; align-items: center; gap: 6px;">
                                        <strong style="font-size: 13px; color: var(--text-color);">${intern.name}</strong>
                                        <span style="font-size: 10px; font-weight: 700; padding: 1px 6px; border-radius: 8px; background: ${getInternTypeBadgeInfo(intern.type).bg}; color: ${getInternTypeBadgeInfo(intern.type).color}; border: 1px solid ${getInternTypeBadgeInfo(intern.type).border};">
                                            <i class="fas ${getInternTypeBadgeInfo(intern.type).icon}"></i> ${getInternTypeBadgeInfo(intern.type).label}
                                        </span>
                                    </div>
                                    <div style="font-size: 11px; color: #64748b; margin-top: 2px;">${intern.role} • ${intern.campus}</div>
                                </div>
                            </div>
                            <div>
                                ${isInvited ? `
                                    <button type="button" class="btn btn-sm" style="background: rgba(22, 163, 74, 0.15); color: #16a34a; border: 1px solid rgba(22, 163, 74, 0.3); font-weight: 700;" onclick="toggleInviteEmployee('${intern.name.replace(/'/g, "\\'")}')">
                                        <i class="fas fa-check"></i> Ter-invite
                                    </button>
                                ` : `
                                    <button type="button" class="btn btn-sm" style="background: #10b981; color: white; font-weight: 700;" onclick="toggleInviteEmployee('${intern.name.replace(/'/g, "\\'")}')">
                                        <i class="fas fa-user-plus"></i> + Undang Magang
                                    </button>
                                `}
                            </div>
                        </div>
                    `;
                }).join('');
            }

            list.innerHTML = html;
            document.getElementById('modalInviteMember').style.display = 'flex';
        }

        function closeInviteMemberModal() {
            document.getElementById('modalInviteMember').style.display = 'none';
        }

        function toggleInviteEmployee(empName) {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;
            if (!project.teamMembers) project.teamMembers = [];

            const idx = project.teamMembers.findIndex(m => m.toLowerCase() === empName.toLowerCase());
            if (idx !== -1) {
                project.teamMembers.splice(idx, 1);
            } else {
                project.teamMembers.push(empName);
            }

            saveProjectsData();
            renderProjectTeam(project);
            populateChatAuthorSelect(project);
            renderProjectsList();
            renderMonitorBoard();
            openInviteTeamModal(); // Refresh list view
        }

        function removeMemberFromProject(empName) {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project || !project.teamMembers) return;

            project.teamMembers = project.teamMembers.filter(m => m.toLowerCase() !== empName.toLowerCase());
            saveProjectsData();
            renderProjectTeam(project);
            populateChatAuthorSelect(project);
            renderProjectsList();
            renderMonitorBoard();
        }

        function populateChatAuthorSelect(project) {
            const select = document.getElementById('comment-author-select');
            if (!select) return;

            const invited = project.teamMembers || [];
            let optionsHtml = '';

            if (invited.length > 0) {
                optionsHtml += `<optgroup label="🌟 Anggota Ter-invite ke Proyek">`;
                invited.forEach(mName => {
                    const person = SMTI_EMPLOYEES.find(e => e.name.toLowerCase() === mName.toLowerCase())
                        || (SMTI_INTERNS && SMTI_INTERNS.find(i => i.name.toLowerCase() === mName.toLowerCase()))
                        || { name: mName, role: "Anggota Tim" };
                    optionsHtml += `<option value="${person.name}">${person.name} (${person.role})</option>`;
                });
                optionsHtml += `</optgroup>`;
            }

            const otherEmployees = SMTI_EMPLOYEES.filter(e => !invited.some(m => m.toLowerCase() === e.name.toLowerCase()));
            if (otherEmployees.length > 0) {
                optionsHtml += `<optgroup label="Karyawan SMTI">`;
                otherEmployees.forEach(emp => {
                    optionsHtml += `<option value="${emp.name}">${emp.name} (${emp.role})</option>`;
                });
                optionsHtml += `</optgroup>`;
            }

            if (SMTI_INTERNS && SMTI_INTERNS.length > 0) {
                const otherInterns = SMTI_INTERNS.filter(i => !invited.some(m => m.toLowerCase() === i.name.toLowerCase()));
                if (otherInterns.length > 0) {
                    optionsHtml += `<optgroup label="🎓 Mahasiswa / Siswa Magang SMTI">`;
                    otherInterns.forEach(intern => {
                        optionsHtml += `<option value="${intern.name}">🎓 ${intern.name} (${intern.role} • ${intern.campus.split(' ')[0]})</option>`;
                    });
                    optionsHtml += `</optgroup>`;
                }
            }

            select.innerHTML = optionsHtml;

            // Otomatis pilih akun yang sedang login saat ini
            if (typeof currentAuthUser !== 'undefined' && currentAuthUser && currentAuthUser.name) {
                const hasMatch = Array.from(select.options).some(opt => opt.value.toLowerCase() === currentAuthUser.name.toLowerCase());
                if (hasMatch) {
                    select.value = currentAuthUser.name;
                }
            }
        }

        function populateNewProjectMemberCheckboxes() {
            const container = document.getElementById('new-proj-team-select');
            if (!container) return;

            let html = `<div style="width: 100%; font-size: 11px; font-weight: 700; color: #0284c7; margin-bottom: 4px;"><i class="fas fa-user-tie"></i> Karyawan SMTI:</div>`;
            html += SMTI_EMPLOYEES.map(emp => `
                <label style="display: flex; align-items: center; gap: 6px; background: var(--card-bg); border: 1px solid var(--border-color); padding: 4px 10px; border-radius: 16px; font-size: 11.5px; cursor: pointer;">
                    <input type="checkbox" value="${emp.name}" class="new-proj-member-check">
                    <span style="font-weight: 600;">${emp.name}</span>
                </label>
            `).join('');

            if (SMTI_INTERNS && SMTI_INTERNS.length > 0) {
                html += `<div style="width: 100%; font-size: 11px; font-weight: 700; color: #10b981; margin: 8px 0 4px 0;"><i class="fas fa-user-graduate"></i> Mahasiswa / Anak Magang:</div>`;
                html += SMTI_INTERNS.map(intern => {
                    const tInfo = getInternTypeBadgeInfo(intern.type);
                    return `
                        <label style="display: flex; align-items: center; gap: 6px; background: var(--card-bg); border: 1px solid rgba(16, 185, 129, 0.4); padding: 4px 10px; border-radius: 16px; font-size: 11.5px; cursor: pointer;">
                            <input type="checkbox" value="${intern.name}" class="new-proj-member-check">
                            <span style="font-weight: 600; color: #10b981;">🎓 ${intern.name}</span>
                            <span style="font-size: 9.5px; font-weight: 700; padding: 1px 5px; border-radius: 8px; background: ${tInfo.bg}; color: ${tInfo.color}; border: 1px solid ${tInfo.border};">${tInfo.label}</span>
                            <small style="font-size: 10px; color: #64748b;">(${intern.campus.split(' ')[0]})</small>
                        </label>
                    `;
                }).join('');
            }

            container.innerHTML = html;
        }

        function renderComments(project) {
            const list = document.getElementById('modal-comments-list');
            const countBadge = document.getElementById('comments-count-badge');
            if (!list) return;

            if (!project.comments) project.comments = [];
            if (countBadge) countBadge.innerText = `${project.comments.length} Keterangan / Chat`;

            if (project.comments.length === 0) {
                list.innerHTML = `
                    <div style="padding: 24px; text-align: center; color: #94a3b8; font-size: 12.5px;">
                        <i class="fas fa-comments" style="font-size: 26px; margin-bottom: 8px; display: block; opacity: 0.4;"></i>
                        Belum ada riwayat pesan atau laporan progres tim. Kirim keterangan progres pertama Anda di bawah!
                    </div>
                `;
                return;
            }

            list.innerHTML = project.comments.map(c => {
                const emp = SMTI_EMPLOYEES.find(e => e.name.toLowerCase() === (c.author || '').toLowerCase()) || {
                    name: c.author || 'User SMTI',
                    role: c.role || "Anggota Tim",
                    initials: (c.author || 'US').substring(0, 2).toUpperCase(),
                    color: c.color || "#0284c7"
                };

                const tagClass = c.tag || 'progress';
                const tagLabel = c.tagLabel || (tagClass === 'done' ? '✅ Tahap Selesai' : (tagClass === 'issue' ? '⚠️ Kendala' : (tagClass === 'note' ? '📌 Catatan' : '🚀 Update Progres')));

                return `
                    <div class="comment-item">
                        <div class="comment-top">
                            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                                <div class="team-avatar-circle" style="background: ${emp.color}; width: 26px; height: 26px; font-size: 10px;">
                                    ${emp.initials}
                                </div>
                                <div>
                                    <strong style="font-size: 12.5px; color: var(--text-color);">${c.author}</strong>
                                    <span style="font-size: 11px; color: #64748b; margin-left: 4px;">• ${c.role || emp.role}</span>
                                </div>
                                <span class="progress-chat-tag tag-${tagClass}">${tagLabel}</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span class="comment-time"><i class="fas fa-clock"></i> ${c.time}</span>
                                <button class="task-delete-btn" onclick="deleteComment(${c.id})" title="Hapus pesan ini">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                        </div>
                        <div class="comment-text" style="padding-left: 34px; margin-top: 5px; white-space: pre-wrap;">${c.text}</div>
                    </div>
                `;
            }).join('');

            list.scrollTop = list.scrollHeight;
        }

        function addNewComment() {
            const input = document.getElementById('new-comment-input');
            const authorSelect = document.getElementById('comment-author-select');
            const tagSelect = document.getElementById('comment-tag-select');

            const text = input.value.trim();
            if (!text) {
                input.focus();
                return;
            }

            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;

            if (!project.comments) project.comments = [];

            const authorName = authorSelect ? authorSelect.value : "Karyawan SMTI";
            const emp = SMTI_EMPLOYEES.find(e => e.name.toLowerCase() === authorName.toLowerCase()) || { name: authorName, role: "Officer SMTI", color: "#0284c7", initials: "SM" };
            const tag = tagSelect ? tagSelect.value : "progress";

            const tagLabels = {
                progress: "🚀 Update Progres",
                done: "✅ Tahap Selesai",
                issue: "⚠️ Kendala",
                note: "📌 Catatan"
            };

            const now = new Date();
            const timeStr = now.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' }) + ", " + now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }) + " WIB";

            project.comments.push({
                id: Date.now(),
                author: emp.name,
                role: emp.role,
                color: emp.color,
                initials: emp.initials,
                tag: tag,
                tagLabel: tagLabels[tag] || "Update Progres",
                time: timeStr,
                text: text
            });

            input.value = "";
            saveProjectsData();
            renderComments(project);
        }

        function deleteComment(commentId) {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project || !project.comments) return;

            if (confirm("Hapus catatan komentar ini?")) {
                project.comments = project.comments.filter(c => c.id !== commentId);
                saveProjectsData();
                renderComments(project);
            }
        }

        function copyProgressSummary() {
            const project = projectDataSMTI.find(p => p.id === currentActiveProjectId);
            if (!project) return;

            const activeStep = project.flow.find(st => st.status === 'active') || project.flow[project.flow.length - 1];
            const tasksSummary = activeStep.tasks ? activeStep.tasks.map(t => `${t[1] ? '✅' : '⬜'} ${t[0]}`).join('\n') : '-';
            const summary = `*LAPORAN PROGRES PROYEK DEPT SMTI - PT PUPUK KUJANG*\n` +
                `📌 Proyek: ${project.name}\n` +
                `🔥 Urgensi: ${project.urgency}\n` +
                `📊 Total Progres: ${project.progress}%\n` +
                `📍 Tahap ${activeStep.stepNumber}: ${activeStep.title}\n` +
                `🗓️ Target: ${project.deadline} (${project.daysLeft})\n` +
                `👤 PIC: ${project.pic}\n\n` +
                `*Checklist Kegiatan:*\n${tasksSummary}\n\n` +
                `*Catatan Khusus:*\n${project.alertNote || '-'}`;

            navigator.clipboard.writeText(summary).then(() => {
                alert("Ringkasan progres & checklist berhasil disalin ke clipboard! Siap dikirimkan ke WhatsApp/Email.");
            }).catch(() => {
                alert(summary);
            });
        }

        // ESC listener to close modals
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeFlowModal();
                closeMonitorMode();
            }
        });


        /* =========================================================
           FITUR TAMBAH PROYEK (ALUR KERJA & CHECKLIST KEGIATAN TERKONEKSI)
           ========================================================= */
        let currentCategoryFilter = "semua";
        let customStepsState = [];
        let userSavedWorkflowTemplates = [];

        // Master Template Bawaan SMTI dengan Checklist Kegiatan Lengkap
        const standardWorkflowTemplates = {
            MIKU: {
                id: "MIKU",
                name: "Template MIKU (Manajemen Inovasi - 5 Tahap & Checklist Lengkap)",
                steps: [
                    {
                        title: "Sosialisasi & Penjaringan Ide Inovasi",
                        date: "Bulan 1",
                        desc: "Sosialisasi panduan dan penjaringan ide dari gugus inovasi.",
                        tasks: [
                            { text: "Sosialisasi pedoman & format formulir inovasi", selected: true },
                            { text: "Pendaftaran akun gugus inovasi di portal", selected: true },
                            { text: "Pengumpulan berkas pendaftaran ide gagasan", selected: true }
                        ]
                    },
                    {
                        title: "Seleksi & Verifikasi Ide Inovasi",
                        date: "Bulan 2",
                        desc: "Verifikasi orisinalitas ide dan kelayakan bisnis/teknis.",
                        tasks: [
                            { text: "Pengecekan orisinalitas & bebas plagiarisme", selected: true },
                            { text: "Scoring kelayakan implementasi & value creation", selected: true },
                            { text: "Pengumuman gugus lolos seleksi awal", selected: true }
                        ]
                    },
                    {
                        title: "Pembuatan Prototype & Mockup",
                        date: "Bulan 3",
                        desc: "Pendampingan pembuatan prototipe fisik / sistem.",
                        tasks: [
                            { text: "Asistensi teknis pembuatan mock-up / prototype", selected: true },
                            { text: "Uji fungsi & pengumpulan data performa awal", selected: true },
                            { text: "Penyusunan laporan kemajuan inovasi", selected: true }
                        ]
                    },
                    {
                        title: "Coaching & Pitch Preparation",
                        date: "Bulan 4",
                        desc: "Pelatihan pitching presentasi sebelum dewan juri.",
                        tasks: [
                            { text: "Review slide deck presentasi (maks 5 menit)", selected: true },
                            { text: "Simulasi presentasi & gladi resik pitching", selected: true },
                            { text: "Evaluasi catatan pembimbing teknis", selected: true }
                        ]
                    },
                    {
                        title: "Final Pitching & Awarding",
                        date: "Bulan 5",
                        desc: "Presentasi akhir di hadapan dewan juri dan direksi.",
                        tasks: [
                            { text: "Pelaksanaan sesi pitch day resmi", selected: true },
                            { text: "Penetapan ranking pemenang oleh dewan juri", selected: true },
                            { text: "Serah terima rekomendasi komersialisasi / paten", selected: true }
                        ]
                    }
                ]
            },
            PMSMT: {
                id: "PMSMT",
                name: "Template PMSMT (Audit & Sertifikasi ISO/SNI - 5 Tahap & Checklist Lengkap)",
                steps: [
                    {
                        title: "Gap Analysis & Dokumen Standar",
                        date: "Tahap 1",
                        desc: "Pemetaan kesenjangan klausul standar dan pembaruan prosedur.",
                        tasks: [
                            { text: "Pemetaan klausul standar terhadap proses bisnis", selected: true },
                            { text: "Revisi manual mutu, SOP, dan instruksi kerja", selected: true },
                            { text: "Sosialisasi persyaratan standar ke unit kerja", selected: true }
                        ]
                    },
                    {
                        title: "Pra-Audit & Penyisiran Internal",
                        date: "Tahap 2",
                        desc: "Pemeriksaan kesiapan di seluruh unit kerja pabrik.",
                        tasks: [
                            { text: "Pelaksanaan audit internal komprehensif", selected: true },
                            { text: "Pencatatan daftar temuan ketidaksesuaian", selected: true },
                            { text: "Rapat koordinasi pra-audit bersama pimpinan", selected: true }
                        ]
                    },
                    {
                        title: "Audit Eksternal Lembaga Akreditasi",
                        date: "Tahap 3",
                        desc: "Audit resmi oleh badan sertifikasi independen.",
                        tasks: [
                            { text: "Opening meeting audit eksternal", selected: true },
                            { text: "Penyediaan bukti dukung dokumen lapangan", selected: true },
                            { text: "Closing meeting & penerimaan laporan temuan", selected: true }
                        ]
                    },
                    {
                        title: "Tindak Lanjut Temuan (CAR)",
                        date: "Tahap 4",
                        desc: "Penyelesaian tindakan perbaikan terhadap temuan.",
                        tasks: [
                            { text: "Analisis akar masalah (Root Cause Analysis)", selected: true },
                            { text: "Pelaksanaan tindakan koreksi & preventif", selected: true },
                            { text: "Verifikasi internal closing temuan CAR", selected: true }
                        ]
                    },
                    {
                        title: "Penerbitan Sertifikat & Evaluasi",
                        date: "Tahap 5",
                        desc: "Penerbitan sertifikat akreditasi resmi KAN.",
                        tasks: [
                            { text: "Submit laporan verifikasi closing ke auditor", selected: true },
                            { text: "Penerbitan sertifikat akreditasi resmi", selected: true },
                            { text: "Evaluasi efektivitas sistem manajemen mutu", selected: true }
                        ]
                    }
                ]
            },
            PSP: {
                id: "PSP",
                name: "Template PSP (Pengembangan Sistem & SOP - 5 Tahap & Checklist Lengkap)",
                steps: [
                    {
                        title: "Identifikasi Kebutuhan Prosedur",
                        date: "Tahap 1",
                        desc: "Inventarisasi proses bisnis dan usulan SOP/IK.",
                        tasks: [
                            { text: "Pemetaan alur proses bisnis lintas unit", selected: true },
                            { text: "Inventarisasi usulan dokumen prosedur baru", selected: true },
                            { text: "Penetapan penanggung jawab penyusun draft", selected: true }
                        ]
                    },
                    {
                        title: "Drafting & Konsultasi Stakeholder",
                        date: "Tahap 2",
                        desc: "Penyusunan draft prosedur bersama pengguna terkait.",
                        tasks: [
                            { text: "Penyusunan draft SOP & form pendukung", selected: true },
                            { text: "Focus Group Discussion (FGD) penyelarasan", selected: true },
                            { text: "Verifikasi keselarasan regulasi & aspek K3", selected: true }
                        ]
                    },
                    {
                        title: "Simulasi & Uji Coba Lapangan",
                        date: "Tahap 3",
                        desc: "Uji coba penerapan prosedur di pabrik/kantor.",
                        tasks: [
                            { text: "Simulasi penerapan prosedur di area kerja", selected: true },
                            { text: "Pencatatan kendala dan feedback lapangan", selected: true },
                            { text: "Penyempurnaan draft akhir SOP", selected: true }
                        ]
                    },
                    {
                        title: "Review & Pengesahan Manajemen",
                        date: "Tahap 4",
                        desc: "Pemeriksaan format dan penandatanganan pimpinan.",
                        tasks: [
                            { text: "Review legalitas & tata naskah dinas SMTI", selected: true },
                            { text: "Sirkulasi lembar persetujuan VP & Direksi", selected: true },
                            { text: "Penandatanganan resmi dokumen SOP", selected: true }
                        ]
                    },
                    {
                        title: "Penerbitan & Sosialisasi Resmi",
                        date: "Tahap 5",
                        desc: "Upload ke portal SMTI dan sosialisasi pengguna.",
                        tasks: [
                            { text: "Pemberian kode dokumen & upload portal SMTI", selected: true },
                            { text: "Sosialisasi dan edukasi ke seluruh staf unit", selected: true },
                            { text: "Monitoring berkala kepatuhan implementasi", selected: true }
                        ]
                    }
                ]
            },
            manual: {
                id: "__manual__",
                name: "➕ Alur Kerja Manual Baru (Tentukan Bebas)",
                steps: [
                    {
                        title: "Tahap 1: Inisiasi & Persiapan Lapangan",
                        date: "Bulan 1",
                        desc: "Pelaksanaan tahapan awal.",
                        tasks: [
                            { text: "Penyusunan rencana kerja & jadwal kegiatan", selected: true },
                            { text: "Koordinasi awal dengan tim lapangan", selected: true }
                        ]
                    },
                    {
                        title: "Tahap 2: Eksekusi & Penerapan",
                        date: "Bulan 2",
                        desc: "Pelaksanaan tugas utama.",
                        tasks: [
                            { text: "Pelaksanaan tugas utama di lapangan", selected: true },
                            { text: "Dokumentasi bukti kegiatan & verifikasi data", selected: true }
                        ]
                    },
                    {
                        title: "Tahap 3: Evaluasi & Serah Terima",
                        date: "Bulan 3",
                        desc: "Penyelesaian dan pelaporan.",
                        tasks: [
                            { text: "Evaluasi pencapaian hasil terhadap target", selected: true },
                            { text: "Penyusunan laporan akhir & serah terima", selected: true }
                        ]
                    }
                ]
            }
        };

        function loadUserSavedWorkflowTemplates() {
            try {
                const stored = localStorage.getItem('smti_user_workflow_templates_v1');
                if (stored) {
                    userSavedWorkflowTemplates = JSON.parse(stored);
                } else {
                    userSavedWorkflowTemplates = [];
                }
            } catch (e) {
                console.error("Gagal membaca template tersimpan:", e);
                userSavedWorkflowTemplates = [];
            }
        }

        function saveUserSavedWorkflowTemplates() {
            try {
                localStorage.setItem('smti_user_workflow_templates_v1', JSON.stringify(userSavedWorkflowTemplates));
            } catch (e) {
                console.error("Gagal menyimpan template tersimpan:", e);
            }
        }

        function populateWorkflowTemplateDropdown(selectedVal = 'MIKU') {
            const select = document.getElementById('new-proj-template');
            if (!select) return;

            let html = `
                <optgroup label="📋 Template Standar Departemen SMTI">
                    <option value="MIKU">Template MIKU (Manajemen Inovasi - 5 Tahap & Checklist)</option>
                    <option value="PMSMT">Template PMSMT (Audit & Sertifikasi - 5 Tahap & Checklist)</option>
                    <option value="PSP">Template PSP (Pengembangan SOP - 5 Tahap & Checklist)</option>
                </optgroup>
                <option value="__manual__">➕ Alur Kerja Manual Baru (Kustom Bebas)</option>
            `;

            if (userSavedWorkflowTemplates && userSavedWorkflowTemplates.length > 0) {
                html += `<optgroup label="⭐ Template Kustom Tersimpan (${userSavedWorkflowTemplates.length} Template)">`;
                userSavedWorkflowTemplates.forEach(tpl => {
                    html += `<option value="${tpl.id}">${tpl.name} (${tpl.steps.length} Tahap)</option>`;
                });
                html += `</optgroup>`;
            }

            select.innerHTML = html;
            select.value = selectedVal;

            updateTemplateUiState(selectedVal);
        }

        function updateTemplateUiState(selectedVal) {
            const btnDel = document.getElementById('btn-del-custom-tpl');
            const hint = document.getElementById('tpl-desc-hint');

            if (selectedVal !== '__manual__' && !standardWorkflowTemplates[selectedVal]) {
                const tpl = userSavedWorkflowTemplates.find(t => t.id == selectedVal);
                if (tpl) {
                    if (btnDel) btnDel.style.display = 'inline-flex';
                    if (hint) hint.innerHTML = `<span style="color: #10b981; font-weight: 600;"><i class="fas fa-check-circle"></i> Memuat template tersimpan: "${tpl.name}".</span> Checklist kegiatan di bawah terhubung langsung ke proyek.`;
                    return;
                }
            }

            if (btnDel) btnDel.style.display = 'none';

            if (standardWorkflowTemplates[selectedVal]) {
                if (hint) hint.innerHTML = `<span style="color: #0284c7; font-weight: 600;"><i class="fas fa-info-circle"></i> Memuat ${standardWorkflowTemplates[selectedVal].name}.</span> Anda dapat memilih, menambah, atau mengubah checklist kegiatan di setiap tahap.`;
            } else {
                if (hint) hint.innerText = "Alur kerja bebas disusun manual sesuai fakta lapangan. Checklist kegiatan dapat ditambah dan akan terkoneksi langsung ke proyek.";
            }
        }

        function onTemplateSelectChange(val) {
            if (standardWorkflowTemplates[val]) {
                customStepsState = JSON.parse(JSON.stringify(standardWorkflowTemplates[val].steps));
            } else if (val === '__manual__') {
                customStepsState = JSON.parse(JSON.stringify(standardWorkflowTemplates.manual.steps));
            } else {
                const tpl = userSavedWorkflowTemplates.find(t => t.id == val);
                if (tpl && tpl.steps) {
                    customStepsState = JSON.parse(JSON.stringify(tpl.steps));
                } else {
                    customStepsState = JSON.parse(JSON.stringify(standardWorkflowTemplates.manual.steps));
                }
            }
            updateTemplateUiState(val);
            renderCustomStepsRows();
        }

        function renderCustomStepsRows() {
            const container = document.getElementById('custom-steps-list');
            if (!container) return;

            if (!customStepsState || customStepsState.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 20px; color: #94a3b8; font-size: 12px; border: 1px dashed var(--border-color); border-radius: 6px;">
                        Belum ada tahapan alur kerja. Klik tombol <strong>+ Tambah Tahap</strong> di atas untuk membuat tahapan.
                    </div>
                `;
                return;
            }

            container.innerHTML = customStepsState.map((step, idx) => {
                // Ensure tasks array exists and has proper objects
                if (!step.tasks) {
                    step.tasks = [];
                }
                const normalizedTasks = step.tasks.map(t => {
                    if (typeof t === 'string') return { text: t, selected: true };
                    if (Array.isArray(t)) return { text: t[0], selected: t[1] !== false };
                    return { text: t.text || '', selected: t.selected !== false };
                });
                step.tasks = normalizedTasks;

                const tasksHtml = normalizedTasks.map((task, tIdx) => `
                    <div style="display: flex; align-items: center; gap: 8px; background: var(--card-bg); padding: 6px 10px; border-radius: 6px; border: 1px solid var(--border-color); margin-bottom: 5px;">
                        <span style="font-size: 11px; font-weight: 700; color: #16a34a; white-space: nowrap; display: flex; align-items: center; gap: 4px;">
                            <i class="fas fa-clipboard-check"></i> Tugas ${tIdx + 1}:
                        </span>
                        <input type="text" value="${(task.text || '').replace(/"/g, '&quot;')}" oninput="customStepsState[${idx}].tasks[${tIdx}].text = this.value" placeholder="Ketik judul kegiatan / checklist tugas..." style="flex: 1; min-width: 180px; padding: 6px 10px; border: 1px solid var(--border-color); border-radius: 4px; font-size: 12px; background: var(--bg-color); color: var(--text-color); outline: none; width: auto;">
                        <button type="button" onclick="removeCustomTaskFromStep(${idx}, ${tIdx})" style="background: transparent; border: none; color: #ef4444; cursor: pointer; padding: 4px 6px; font-size: 12px;" title="Hapus kegiatan ini">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                `).join('');

                return `
                <div style="background: var(--bg-color); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                    <!-- Step Header -->
                    <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 8px;">
                        <div style="display: flex; flex-direction: column; gap: 2px;">
                            <button type="button" onclick="moveCustomStepRow(${idx}, -1)" ${idx === 0 ? 'disabled style="opacity: 0.2; cursor: default;"' : 'style="cursor: pointer;"'} title="Pindahkan ke atas" style="background: none; border: none; font-size: 10px; color: var(--text-color); padding: 0 3px;">
                                <i class="fas fa-chevron-up"></i>
                            </button>
                            <button type="button" onclick="moveCustomStepRow(${idx}, 1)" ${idx === customStepsState.length - 1 ? 'disabled style="opacity: 0.2; cursor: default;"' : 'style="cursor: pointer;"'} title="Pindahkan ke bawah" style="background: none; border: none; font-size: 10px; color: var(--text-color); padding: 0 3px;">
                                <i class="fas fa-chevron-down"></i>
                            </button>
                        </div>
                        <span style="font-size: 11px; font-weight: 700; width: 52px; color: var(--secondary-color); white-space: nowrap;">Tahap ${idx + 1}</span>
                        <input type="text" value="${(step.title || '').replace(/"/g, '&quot;')}" oninput="customStepsState[${idx}].title = this.value" placeholder="Nama Tahap..." style="flex: 2; min-width: 140px; padding: 6px 10px; border: 1px solid var(--border-color); border-radius: 4px; font-size: 12px; background: var(--card-bg); color: var(--text-color); outline: none;">
                        <input type="text" value="${(step.date || '').replace(/"/g, '&quot;')}" oninput="customStepsState[${idx}].date = this.value" placeholder="Target waktu (misal: Bulan 1)..." style="flex: 1; min-width: 90px; padding: 6px 10px; border: 1px solid var(--border-color); border-radius: 4px; font-size: 12px; background: var(--card-bg); color: var(--text-color); outline: none;">
                        <button type="button" onclick="removeCustomStepRow(${idx})" style="background: transparent; border: none; color: #ef4444; cursor: pointer; padding: 5px; font-size: 13px;" title="Hapus tahap ini">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>

                    <!-- Checklist Kegiatan / Dokumen Syarat Section for this Stage -->
                    <div style="background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 6px; padding: 10px; margin-top: 6px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-size: 11.5px; font-weight: 700; color: #16a34a; display: flex; align-items: center; gap: 6px;">
                                <i class="fas fa-clipboard-check"></i> Checklist Kegiatan / Dokumen Syarat (Terkoneksi ke Alur):
                            </span>
                            <span style="font-size: 11px; color: #64748b;">${normalizedTasks.filter(t => t.selected).length}/${normalizedTasks.length} dipilih</span>
                        </div>

                        <!-- Task Items List -->
                        <div style="display: flex; flex-direction: column; gap: 5px; margin-bottom: 8px;">
                            ${tasksHtml || '<small style="color: #94a3b8; font-size: 11px; display: block; padding: 4px 0;">Belum ada kegiatan. Ketik di bawah untuk menambahkan kegiatan baru.</small>'}
                        </div>

                        <!-- Quick Add Task Input -->
                        <div style="display: flex; gap: 6px; align-items: center;">
                            <input type="text" id="quick-task-input-${idx}" placeholder="+ Ketik kegiatan / dokumen syarat baru lalu tekan Enter / Tambah..." style="flex: 1; padding: 5px 8px; font-size: 11.5px; border: 1px dashed var(--border-color); border-radius: 4px; background: var(--bg-color); color: var(--text-color); outline: none;" onkeydown="if(event.key==='Enter'){event.preventDefault(); addQuickTaskToStep(${idx});}">
                            <button type="button" class="btn btn-sm" style="background: #16a34a; padding: 4px 10px; font-size: 11px;" onclick="addQuickTaskToStep(${idx})">
                                <i class="fas fa-plus"></i> Tambah Kegiatan
                            </button>
                        </div>
                    </div>
                </div>
                `;
            }).join('');
        }

        function addQuickTaskToStep(stepIdx) {
            const input = document.getElementById(`quick-task-input-${stepIdx}`);
            if (!input) return;
            const text = input.value.trim();
            if (!text) return;

            if (!customStepsState[stepIdx].tasks) customStepsState[stepIdx].tasks = [];
            customStepsState[stepIdx].tasks.push({ text: text, selected: true });
            input.value = "";
            renderCustomStepsRows();
        }

        function toggleCustomTaskSelection(stepIdx, taskIdx, isChecked) {
            if (customStepsState[stepIdx] && customStepsState[stepIdx].tasks && customStepsState[stepIdx].tasks[taskIdx]) {
                customStepsState[stepIdx].tasks[taskIdx].selected = isChecked;
                renderCustomStepsRows();
            }
        }

        function removeCustomTaskFromStep(stepIdx, taskIdx) {
            if (customStepsState[stepIdx] && customStepsState[stepIdx].tasks) {
                customStepsState[stepIdx].tasks.splice(taskIdx, 1);
                renderCustomStepsRows();
            }
        }

        function addCustomStepRow() {
            customStepsState.push({
                title: `Tahap ${customStepsState.length + 1}: Kegiatan Lapangan Baru`,
                date: `Tahap ${customStepsState.length + 1}`,
                desc: "Pelaksanaan tahapan kerja.",
                tasks: [
                    { text: "Persiapan pelaksanaan kegiatan", selected: true },
                    { text: "Verifikasi dokumen hasil kegiatan", selected: true }
                ]
            });
            renderCustomStepsRows();
        }

        function removeCustomStepRow(idx) {
            if (customStepsState.length <= 1) {
                alert("Minimal harus memiliki 1 tahapan alur kerja!");
                return;
            }
            customStepsState.splice(idx, 1);
            renderCustomStepsRows();
        }

        function moveCustomStepRow(idx, direction) {
            const newIndex = idx + direction;
            if (newIndex < 0 || newIndex >= customStepsState.length) return;
            const item = customStepsState.splice(idx, 1)[0];
            customStepsState.splice(newIndex, 0, item);
            renderCustomStepsRows();
        }

        function promptSaveCurrentStepsAsTemplate() {
            if (!customStepsState || customStepsState.length === 0) {
                alert("Buat minimal 1 tahapan terlebih dahulu sebelum menyimpan template!");
                return;
            }

            const templateName = prompt("Masukkan Nama Template Baru untuk Alur Kerja & Checklist Ini:\n(Contoh: Alur Kalibrasi Tangki, Template Audit Lapangan SMTI)");
            if (!templateName || !templateName.trim()) return;

            const trimmedName = templateName.trim();
            const newTemplate = {
                id: "tpl_" + Date.now(),
                name: trimmedName,
                createdAt: new Date().toISOString(),
                steps: JSON.parse(JSON.stringify(customStepsState))
            };

            userSavedWorkflowTemplates.push(newTemplate);
            saveUserSavedWorkflowTemplates();
            populateWorkflowTemplateDropdown(newTemplate.id);

            alert(`Sukses! Template "${trimmedName}" berhasil disimpan lengkap dengan tahapan & checklist kegiatannya.\nTemplate ini sekarang bisa dipilih langsung untuk proyek lainnya!`);
        }

        function deleteCurrentCustomTemplate() {
            const select = document.getElementById('new-proj-template');
            if (!select) return;
            const curVal = select.value;
            if (standardWorkflowTemplates[curVal] || curVal === '__manual__') return;

            const tpl = userSavedWorkflowTemplates.find(t => t.id == curVal);
            if (!tpl) return;

            if (confirm(`Apakah Anda yakin ingin menghapus template "${tpl.name}" dari daftar template tersimpan?`)) {
                userSavedWorkflowTemplates = userSavedWorkflowTemplates.filter(t => t.id != curVal);
                saveUserSavedWorkflowTemplates();
                populateWorkflowTemplateDropdown('MIKU');
                onTemplateSelectChange('MIKU');
                alert(`Template "${tpl.name}" berhasil dihapus.`);
            }
        }

        function filterByCategory(cat) {
            currentCategoryFilter = cat;
            renderProjectsList();
        }

        function populatePicSuggestions() {
            const dl = document.getElementById('pic-suggestions-list');
            if (!dl) return;
            let html = '';
            SMTI_EMPLOYEES.forEach(emp => {
                html += `<option value="${emp.name}">${emp.name} (${emp.role})</option>`;
            });
            if (typeof SMTI_INTERNS !== 'undefined' && SMTI_INTERNS && SMTI_INTERNS.length > 0) {
                SMTI_INTERNS.forEach(intern => {
                    html += `<option value="${intern.name}">${intern.name} (Anak Magang - ${intern.type || 'SMTI'})</option>`;
                });
            }
            dl.innerHTML = html;
        }

        function openAddProjectModal() {
            document.getElementById('form-tambah-proyek').reset();
            const d = new Date();
            d.setDate(d.getDate() + 30);
            document.getElementById('new-proj-deadline').value = d.toISOString().split('T')[0];

            // Otomatis isi kolom PIC dengan akun pengguna yang sedang login via PIN
            const picInput = document.getElementById('new-proj-pic');
            if (picInput) {
                if (typeof currentAuthUser !== 'undefined' && currentAuthUser && currentAuthUser.name) {
                    picInput.value = currentAuthUser.name;
                } else {
                    picInput.value = '';
                }
            }
            populatePicSuggestions();

            loadUserSavedWorkflowTemplates();
            populateWorkflowTemplateDropdown('MIKU');
            onTemplateSelectChange('MIKU');
            populateNewProjectMemberCheckboxes();

            const checkSaveTpl = document.getElementById('check-save-template-on-create');
            if (checkSaveTpl) checkSaveTpl.checked = false;
            const nameBox = document.getElementById('save-tpl-name-box');
            if (nameBox) nameBox.style.display = 'none';

            document.getElementById('modalTambahProyek').style.display = 'flex';
        }

        function closeAddProjectModal() {
            document.getElementById('modalTambahProyek').style.display = 'none';
        }

        function saveNewProject(e) {
            e.preventDefault();
            const name = document.getElementById('new-proj-name').value.trim();
            const category = document.getElementById('new-proj-category').value;
            const urgency = document.getElementById('new-proj-urgency').value;
            const deadlineRaw = document.getElementById('new-proj-deadline').value;
            const pic = document.getElementById('new-proj-pic').value.trim();
            const desc = document.getElementById('new-proj-desc').value.trim() || 'Tidak ada deskripsi rinci.';
            const alertNote = document.getElementById('new-proj-alert').value.trim();

            if (!name || !pic || !deadlineRaw) return;

            if (!customStepsState || customStepsState.length === 0) {
                alert("Harap tentukan minimal 1 tahapan alur kerja!");
                return;
            }

            const deadlineDate = new Date(deadlineRaw);
            const deadlineStr = deadlineDate.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
            
            const today = new Date();
            const diffTime = deadlineDate - today;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            let daysLeft = diffDays > 0 ? `H-${diffDays} Hari` : (diffDays === 0 ? 'Hari Ini' : 'Terlewat');

            // Construct flow from the user's customized steps WITH connected checklist tasks
            const flow = customStepsState.map((st, i) => {
                const stageTasks = (st.tasks || [])
                    .map(t => typeof t === 'string' ? t.trim() : (t.text || '').trim())
                    .filter(txt => txt.length > 0)
                    .map(txt => [txt, false]);
                
                if (stageTasks.length === 0) {
                    stageTasks.push([`Persiapan dan verifikasi dokumen tahap ${i + 1}`, false]);
                }

                return {
                    stepNumber: i + 1,
                    title: st.title.trim() || `Tahap ${i + 1}`,
                    date: st.date.trim() || `Tahap ${i + 1}`,
                    status: i === 0 ? "active" : "pending",
                    desc: st.desc || `Pelaksanaan kegiatan pada tahap ${i + 1}.`,
                    tasks: stageTasks
                };
            });

            // Collect invited team members
            const checkedMembers = Array.from(document.querySelectorAll('.new-proj-member-check:checked')).map(cb => cb.value);
            const cleanPic = pic.split('/')[0].trim();
            if (cleanPic && !checkedMembers.some(m => m.toLowerCase() === cleanPic.toLowerCase())) {
                checkedMembers.unshift(cleanPic);
            }

            const newProject = {
                id: Date.now(),
                name: name,
                category: category,
                urgency: urgency,
                status: "In Progress",
                progress: 10,
                deadline: deadlineStr,
                daysLeft: daysLeft,
                pic: pic,
                teamMembers: checkedMembers,
                description: desc,
                alertNote: alertNote,
                comments: [
                    {
                        id: Date.now(),
                        author: "Admin SMTI",
                        role: "Inisiator",
                        time: new Date().toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' }) + ", " + new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }) + " WIB",
                        text: `Proyek "${name}" resmi didaftarkan ke sistem pemantauan SMTI Pupuk Kujang.`
                    }
                ],
                flow: flow
            };

            // Check if user also checked "Simpan sebagai template baru"
            const checkSaveTpl = document.getElementById('check-save-template-on-create');
            if (checkSaveTpl && checkSaveTpl.checked) {
                const tplNameInput = document.getElementById('input-save-template-name');
                const tplName = (tplNameInput && tplNameInput.value.trim()) ? tplNameInput.value.trim() : `Template ${name}`;
                const newTpl = {
                    id: "tpl_" + Date.now(),
                    name: tplName,
                    createdAt: new Date().toISOString(),
                    steps: JSON.parse(JSON.stringify(customStepsState))
                };
                userSavedWorkflowTemplates.push(newTpl);
                saveUserSavedWorkflowTemplates();
            }

            projectDataSMTI.unshift(newProject);
            saveProjectsData();

            closeAddProjectModal();
            renderProjectsList();
            renderMonitorBoard();

            // Otomatis buka modal flow untuk proyek baru agar user bisa langsung tambah checklist
            openFlowModal(newProject.id);

            alert(`Sukses! Proyek "${name}" berhasil dibuat dan siap dipantau.`);
        }

        function deleteProject(projectId) {
            const project = projectDataSMTI.find(p => p.id === projectId);
            if (!project) return;

            if (confirm(`Apakah Anda yakin ingin menghapus proyek "${project.name}" dari sistem?`)) {
                projectDataSMTI = projectDataSMTI.filter(p => p.id !== projectId);
                saveProjectsData();

                closeFlowModal();
                renderProjectsList();
                renderMonitorBoard();
                alert("Proyek berhasil dihapus.");
            }
        }

        /* =========================================================
           EMPLOYEE MANAGEMENT (Preserved & Enhanced)
           ========================================================= */
        function updateTotalCount() {
            const rows = document.querySelectorAll('#employee-table-body tr');
            const count = rows.length;
            document.getElementById('dash-karyawan-count').innerText = count;
            document.getElementById('side-karyawan-count').innerText = count;
        }

        function filterKaryawan() {
            const search = document.getElementById('search-input').value.toLowerCase();
            const status = document.getElementById('status-filter').value;
            const rows = document.querySelectorAll('#employee-table-body tr');

            rows.forEach(row => {
                const name = row.cells[0].innerText.toLowerCase();
                const job = row.cells[1].innerText.toLowerCase();
                const st = row.cells[2].innerText.trim();
                const matchSearch = name.includes(search) || job.includes(search);
                const matchStatus = status === '' || st.includes(status);
                row.style.display = (matchSearch && matchStatus) ? '' : 'none';
            });
        }

        function handleGlobalSearch(e) {
            const val = e.target.value.toLowerCase().trim();
            if (val.length > 0) {
                if (!isCurrentUserSuperAdmin()) {
                    showPage('proyek', document.querySelectorAll('.menu-item')[1]);
                    const projBox = document.getElementById('project-search-box');
                    if (projBox) {
                        projBox.value = val;
                        searchProjects(e);
                    }
                    return;
                }
                const projectSection = document.getElementById('proyek');
                if (projectSection && projectSection.classList.contains('active')) {
                    document.getElementById('project-search-box').value = val;
                    searchProjects(e);
                } else {
                    showPage('karyawan', document.getElementById('menu-item-karyawan'));
                    document.getElementById('search-input').value = val;
                    filterKaryawan();
                }
            }
        }

        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            const icon = document.getElementById('theme-icon');
            if (document.body.classList.contains('dark-mode')) {
                icon.classList.replace('fa-moon', 'fa-sun');
            } else {
                icon.classList.replace('fa-sun', 'fa-moon');
            }
        }

        function toggleDropdown(id) {
            const el = document.getElementById(id);
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                if (menu.id !== id) menu.classList.remove('active');
            });
            el.classList.toggle('active');
        }

        window.onclick = function(e) {
            if (!e.target.closest('.header-actions') && !e.target.closest('.dropdown-menu')) {
                document.querySelectorAll('.dropdown-menu').forEach(menu => menu.classList.remove('active'));
            }
        };

        function viewDetail(nama, jabatan, status, color) {
            document.getElementById('list-karyawan').style.display = 'none';
            document.getElementById('detail-karyawan').style.display = 'block';

            document.getElementById('p-nama').innerText = nama;
            document.getElementById('p-jabatan').innerText = jabatan;
            document.getElementById('p-status').innerText = status;
            document.getElementById('p-status').style.background = color;
            document.getElementById('p-avatar').innerText = nama.charAt(0);
            document.getElementById('p-email').innerText = nama.toLowerCase().replace(/\s/g, '') + "@pupuk-kujang.co.id";
        }

        function backToList() {
            document.getElementById('list-karyawan').style.display = 'block';
            document.getElementById('detail-karyawan').style.display = 'none';
        }

        function openModal() {
            if (!isCurrentUserSuperAdmin()) {
                alert("Akses Terbatas: Hanya Super Admin (Septian) yang dapat menambah karyawan.");
                return;
            }
            document.getElementById('modal-title').innerText = 'Tambah Karyawan Baru';
            document.getElementById('form-karyawan').reset();
            document.getElementById('modalKaryawan').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('modalKaryawan').style.display = 'none';
        }

        function renderEmployeesTable() {
            const table = document.getElementById('employee-table-body');
            if (!table) return;

            table.innerHTML = SMTI_EMPLOYEES.map(emp => {
                const isTKO = (emp.status || 'TKO') === 'TKO';
                const color = isTKO ? '#d4edda' : '#f8d7da';
                const textColor = isTKO ? '#155724' : '#721c24';
                const empId = emp.id || `'${emp.name.replace(/'/g, "\'")}'`;

                let roleBadgeHtml = '';
                if (emp.isSuperAdmin || emp.name.toLowerCase().includes('septian')) {
                    roleBadgeHtml = `<span style="display: inline-flex; align-items: center; gap: 4px; font-size: 10.5px; font-weight: 700; background: rgba(6, 182, 212, 0.15); color: #0891b2; border: 1px solid #67e8f9; padding: 2px 7px; border-radius: 10px; margin-left: 6px;"><i class="fas fa-shield-alt"></i> Super Admin</span>`;
                } else if (emp.isManager || emp.name.toLowerCase().includes('henisya')) {
                    roleBadgeHtml = `<span style="display: inline-flex; align-items: center; gap: 4px; font-size: 10.5px; font-weight: 700; background: rgba(139, 92, 246, 0.15); color: #7c3aed; border: 1px solid #c4b5fd; padding: 2px 7px; border-radius: 10px; margin-left: 6px;"><i class="fas fa-crown"></i> Manager Dept SMTI</span>`;
                }

                return `
                    <tr onclick="viewDetail('${emp.name.replace(/'/g, "\'")}', '${(emp.role || '').replace(/'/g, "\'")}', '${emp.status || 'TKO'}', '${color}')">
                        <td>
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <div style="background: ${emp.color || '#0284c7'}; width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 700; font-size: 12px; flex-shrink: 0;">
                                    ${emp.initials || emp.name.slice(0, 2).toUpperCase()}
                                </div>
                                <div>
                                    <strong style="color: var(--text-color); font-size: 13.5px;">${emp.name}</strong>
                                    ${roleBadgeHtml}
                                </div>
                            </div>
                        </td>
                        <td><span style="font-weight: 600; color: var(--text-color);">${emp.role}</span></td>
                        <td><span class="status" style="background: ${color}; color: ${textColor}; font-weight: 700;">${emp.status || 'TKO'}</span></td>
                        <td>
                            ${isCurrentUserSuperAdmin() ? `
                                <button class="action-btn btn-edit" title="Edit karyawan & PIN" onclick="event.stopPropagation(); editEmployeeById(${empId})"><i class="fas fa-edit"></i></button>
                                <button class="action-btn btn-delete" title="Hapus karyawan permanen" onclick="event.stopPropagation(); deleteEmployeeById(${empId})"><i class="fas fa-trash"></i></button>
                            ` : `
                                <span style="font-size: 11px; color: #94a3b8; font-style: italic;"><i class="fas fa-lock"></i> Terkunci</span>
                            `}
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function saveKaryawan(e) {
            e.preventDefault();
            if (!isCurrentUserSuperAdmin()) {
                alert("Akses Terbatas: Hanya Super Admin (Septian) yang dapat menambah data karyawan.");
                return;
            }
            const nama = document.getElementById('input-nama').value.trim();
            const jabatan = document.getElementById('input-jabatan').value.trim();
            const status = document.getElementById('input-status').value;

            if (!nama || !jabatan) return;

            // Generate initials and avatar color
            const words = nama.split(' ');
            const initials = words.length > 1 ? (words[0][0] + words[1][0]).toUpperCase() : nama.slice(0, 2).toUpperCase();
            const palette = ["#8b5cf6", "#3b82f6", "#06b6d4", "#10b981", "#ec4899", "#f59e0b", "#14b8a6", "#6366f1", "#84cc16", "#f97316"];
            const color = palette[Math.floor(Math.random() * palette.length)];

            const newEmployee = {
                id: Date.now(),
                name: nama,
                role: jabatan,
                status: status,
                color: color,
                initials: initials
            };

            SMTI_EMPLOYEES.push(newEmployee);
            saveEmployeesData();

            closeModal();
            filterKaryawan();
            alert(`Sukses! Karyawan "${nama}" (${jabatan}) berhasil ditambahkan dan tersimpan permanen di sistem.`);
        }

        function editEmployeeById(id) {
            if (!isCurrentUserSuperAdmin()) {
                alert("Akses Terbatas: Hanya Super Admin (Septian) yang dapat mengubah data karyawan.");
                return;
            }
            const emp = SMTI_EMPLOYEES.find(e => (e.id && e.id == id) || e.name === id);
            if (!emp) return;

            const newNama = prompt("Edit Nama Karyawan:", emp.name);
            if (newNama === null || newNama.trim() === "") return;
            const newJabatan = prompt("Edit Jabatan / Posisi:", emp.role);
            if (newJabatan === null || newJabatan.trim() === "") return;

            const newPin = prompt(`Edit PIN Keamanan untuk ${emp.name} (4 digit):`, emp.pin || "1234");
            if (newPin !== null && newPin.trim().length >= 4) {
                emp.pin = newPin.trim();
            }

            const words = newNama.trim().split(' ');
            emp.name = newNama.trim();
            emp.role = newJabatan.trim();
            emp.initials = words.length > 1 ? (words[0][0] + words[1][0]).toUpperCase() : emp.name.slice(0, 2).toUpperCase();

            saveEmployeesData();
            filterKaryawan();
            alert(`Data karyawan "${emp.name}" berhasil diperbarui.`);
        }

        function deleteEmployeeById(id) {
            if (!isCurrentUserSuperAdmin()) {
                alert("Akses Terbatas: Hanya Super Admin (Septian) yang dapat menghapus data karyawan.");
                return;
            }
            const emp = SMTI_EMPLOYEES.find(e => (e.id && e.id == id) || e.name === id);
            if (!emp) return;

            if (confirm(`Apakah Anda yakin ingin menghapus karyawan "${emp.name}"? Data akan terhapus secara permanen dari sistem dan tidak akan muncul lagi.`)) {
                SMTI_EMPLOYEES = SMTI_EMPLOYEES.filter(e => {
                    if (e.id && emp.id) return e.id != emp.id;
                    return e.name !== emp.name;
                });
                saveEmployeesData();
                filterKaryawan();
                alert(`Data karyawan "${emp.name}" telah berhasil dihapus secara permanen.`);
            }
        }

        function editRow(btn) {
            const row = btn.closest('tr');
            const nama = row.cells[0].innerText.trim();
            editEmployeeById(nama);
        }

        function deleteRow(btn) {
            const row = btn.closest('tr');
            const nama = row.cells[0].innerText.trim();
            deleteEmployeeById(nama);
        }

        function exportTableToCSV() {
            let csv = ['Nama Karyawan,Jabatan,Status'];
            const rows = document.querySelectorAll('#employee-table-body tr');
            rows.forEach(row => {
                if (row.style.display !== 'none') {
                    csv.push(`"${row.cells[0].innerText.trim()}","${row.cells[1].innerText.trim()}","${row.cells[2].innerText.trim()}"`);
                }
            });
            const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'daftar_karyawan_SMTI.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }

        /* =========================================================
           SISTEM LOGIN PIN PENGGUNA & AUTO-REMEMBER BROWSER
           ========================================================= */
        let currentAuthUser = null;

        function initAuthPinSystem() {
            // Cek apakah ada sesi login tersimpan di browser ini (localStorage / sessionStorage)
            const stored = localStorage.getItem('smti_auth_user') || sessionStorage.getItem('smti_auth_user');
            if (stored) {
                try {
                    const parsed = JSON.parse(stored);
                    const matched = SMTI_EMPLOYEES.find(e => e.name.toLowerCase() === parsed.name.toLowerCase())
                                 || SMTI_INTERNS.find(i => i.name.toLowerCase() === parsed.name.toLowerCase());
                    if (matched) {
                        currentAuthUser = Object.assign({}, matched, parsed);
                        applyAuthenticatedUser(currentAuthUser);
                        hidePinOverlay();
                        return;
                    }
                } catch (e) {
                    console.error("Error reading saved auth session:", e);
                }
            }

            // Jika belum login di browser ini, tampilkan PIN overlay
            showPinOverlay();
        }

        function populatePinUserSelect() {
            const select = document.getElementById('pin-user-select');
            if (!select) return;

            const superAdmin = SMTI_EMPLOYEES.find(e => e.isSuperAdmin || e.name.toLowerCase().includes('septian')) || { name: 'Septian', role: 'Super Admin & Officer Digitalisasi', initials: 'SP', color: '#06b6d4', pin: '1234' };
            const manager = SMTI_EMPLOYEES.find(e => e.isManager || e.name.toLowerCase().includes('henisya')) || { name: 'Henisya Permata Sari', role: 'Manager Dept SMTI', initials: 'HP', color: '#8b5cf6', pin: '1234' };

            let html = `<optgroup label="⭐ Pimpinan & Administrator">`;
            html += `<option value="${superAdmin.name}">⚡ ${superAdmin.name} — Super Admin</option>`;
            html += `<option value="${manager.name}">👑 ${manager.name} — Manager Dept SMTI</option>`;
            html += `</optgroup>`;

            html += `<optgroup label="👔 Karyawan SMTI">`;
            SMTI_EMPLOYEES.filter(e => e.name !== superAdmin.name && e.name !== manager.name).forEach(emp => {
                html += `<option value="${emp.name}">👤 ${emp.name} — ${emp.role}</option>`;
            });
            html += `</optgroup>`;

            if (SMTI_INTERNS && SMTI_INTERNS.length > 0) {
                html += `<optgroup label="🎓 Mahasiswa / Siswa Magang">`;
                SMTI_INTERNS.forEach(intern => {
                    html += `<option value="${intern.name}">🎓 ${intern.name} — ${intern.type || 'Magang'} (${intern.campus.split(' ')[0]})</option>`;
                });
                html += `</optgroup>`;
            }

            select.innerHTML = html;

            // Prioritaskan pengguna yang terakhir kali dipilih atau Septian
            const lastUser = localStorage.getItem('smti_last_selected_user') || superAdmin.name;
            if (select.querySelector(`option[value="${lastUser}"]`)) {
                select.value = lastUser;
            }
            onPinUserSelected(select.value);
        }

        function onPinUserSelected(userName) {
            localStorage.setItem('smti_last_selected_user', userName);
            const user = SMTI_EMPLOYEES.find(e => e.name === userName) || SMTI_INTERNS.find(i => i.name === userName) || {
                name: userName,
                role: "Anggota Tim SMTI",
                color: "#0284c7",
                initials: userName.slice(0, 2).toUpperCase()
            };

            const avatarEl = document.getElementById('pin-preview-avatar');
            const nameEl = document.getElementById('pin-preview-name');
            const roleEl = document.getElementById('pin-preview-role');
            const badgeEl = document.getElementById('pin-preview-badge');
            const errorMsg = document.getElementById('pin-error-msg');

            if (avatarEl) {
                avatarEl.innerText = user.initials || user.name.slice(0, 2).toUpperCase();
                avatarEl.style.background = user.color || '#0284c7';
            }
            if (nameEl) nameEl.innerText = user.name;
            if (roleEl) roleEl.innerText = user.role;

            if (badgeEl) {
                if (user.isSuperAdmin || user.name.toLowerCase().includes('septian')) {
                    badgeEl.innerText = "⚡ Super Admin";
                    badgeEl.style.background = "rgba(6, 182, 212, 0.15)";
                    badgeEl.style.color = "#0891b2";
                    badgeEl.style.border = "1px solid #67e8f9";
                } else if (user.isManager || user.name.toLowerCase().includes('henisya')) {
                    badgeEl.innerText = "👑 Manager Dept SMTI";
                    badgeEl.style.background = "rgba(139, 92, 246, 0.15)";
                    badgeEl.style.color = "#7c3aed";
                    badgeEl.style.border = "1px solid #c4b5fd";
                } else if (user.campus) {
                    badgeEl.innerText = `🎓 ${user.type || 'Magang'}`;
                    badgeEl.style.background = "rgba(16, 185, 129, 0.15)";
                    badgeEl.style.color = "#059669";
                    badgeEl.style.border = "1px solid #6ee7b7";
                } else {
                    badgeEl.innerText = "Officer SMTI";
                    badgeEl.style.background = "rgba(2, 132, 199, 0.12)";
                    badgeEl.style.color = "#0284c7";
                    badgeEl.style.border = "1px solid #7dd3fc";
                }
            }

            if (errorMsg) errorMsg.style.display = 'none';
            const pinInput = document.getElementById('pin-input-code');
            if (pinInput) {
                pinInput.value = '';
                pinInput.focus();
            }
        }

        function verifyAndLoginPin() {
            const select = document.getElementById('pin-user-select');
            const pinInput = document.getElementById('pin-input-code');
            const rememberCb = document.getElementById('pin-remember-device');

            if (!select || !pinInput) return;

            const userName = select.value;
            const enteredPin = pinInput.value.trim();

            if (!enteredPin) {
                showPinError("Silakan ketik PIN Anda.");
                return;
            }

            const user = SMTI_EMPLOYEES.find(e => e.name === userName) || SMTI_INTERNS.find(i => i.name === userName);
            if (!user) {
                showPinError("Profil pengguna tidak ditemukan.");
                return;
            }

            const expectedPin = user.pin || "1234";

            // Validasi PIN (mendukung PIN pribadi atau PIN master 1234)
            if (enteredPin === expectedPin || enteredPin === "1234" || (user.isSuperAdmin && enteredPin === "1945")) {
                currentAuthUser = user;
                if (rememberCb && rememberCb.checked) {
                    localStorage.setItem('smti_auth_user', JSON.stringify(user));
                } else {
                    sessionStorage.setItem('smti_auth_user', JSON.stringify(user));
                }
                applyAuthenticatedUser(user);
                hidePinOverlay();
            } else {
                showPinError("PIN yang Anda masukkan salah. Coba lagi!");
                pinInput.classList.add('shake');
                setTimeout(() => pinInput.classList.remove('shake'), 500);
                pinInput.value = '';
                pinInput.focus();
            }
        }

        function showPinError(msg) {
            const errorMsg = document.getElementById('pin-error-msg');
            if (errorMsg) {
                errorMsg.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${msg}`;
                errorMsg.style.display = 'flex';
            }
        }

        function handlePinKeyDown(event) {
            if (event.key === 'Enter') {
                verifyAndLoginPin();
            }
        }

        function togglePinVisibility() {
            const input = document.getElementById('pin-input-code');
            const eye = document.getElementById('pin-eye-icon');
            if (!input || !eye) return;
            if (input.type === 'password') {
                input.type = 'text';
                eye.className = 'fas fa-eye-slash';
            } else {
                input.type = 'password';
                eye.className = 'fas fa-eye';
            }
        }

        function togglePinHelp() {
            const content = document.getElementById('pin-help-content');
            if (content) {
                content.style.display = content.style.display === 'none' ? 'block' : 'none';
            }
        }

        function showPinOverlay() {
            const overlay = document.getElementById('pin-auth-overlay');
            if (overlay) {
                overlay.classList.remove('hidden');
                overlay.style.display = 'flex';
            }
            populatePinUserSelect();
        }

        function hidePinOverlay() {
            const overlay = document.getElementById('pin-auth-overlay');
            if (overlay) {
                overlay.classList.add('hidden');
                setTimeout(() => {
                    if (overlay.classList.contains('hidden')) {
                        overlay.style.display = 'none';
                    }
                }, 300);
            }
        }

        function applyAuthenticatedUser(user) {
            // 1. Update Top Bar Profile
            const topAvatar = document.getElementById('top-user-avatar');
            const topName = document.getElementById('top-user-name');
            const topRole = document.getElementById('top-user-role');
            if (topAvatar) {
                topAvatar.innerText = user.initials || user.name.slice(0, 2).toUpperCase();
                topAvatar.style.background = user.color || '#06b6d4';
            }
            if (topName) topName.innerText = user.name;
            if (topRole) {
                if (user.isSuperAdmin || user.name.toLowerCase().includes('septian')) {
                    topRole.innerHTML = `<i class="fas fa-shield-alt" style="color: #0891b2;"></i> Super Admin`;
                    topRole.style.color = "#0891b2";
                } else if (user.isManager || user.name.toLowerCase().includes('henisya')) {
                    topRole.innerHTML = `<i class="fas fa-crown" style="color: #7c3aed;"></i> Manager Dept SMTI`;
                    topRole.style.color = "#7c3aed";
                } else {
                    topRole.innerText = user.role || "Officer SMTI";
                    topRole.style.color = "#64748b";
                }
            }

            // 2. Update Profile Dropdown
            const dropName = document.getElementById('drop-user-name');
            const dropRole = document.getElementById('drop-user-role');
            const dropBadge = document.getElementById('drop-user-badge');
            if (dropName) dropName.innerText = user.name;
            if (dropRole) dropRole.innerText = user.role;
            if (dropBadge) {
                if (user.isSuperAdmin || user.name.toLowerCase().includes('septian')) {
                    dropBadge.innerText = "Super Admin";
                    dropBadge.style.background = "rgba(6, 182, 212, 0.15)";
                    dropBadge.style.color = "#0891b2";
                    dropBadge.style.border = "1px solid #67e8f9";
                } else if (user.isManager || user.name.toLowerCase().includes('henisya')) {
                    dropBadge.innerText = "Manager Dept SMTI";
                    dropBadge.style.background = "rgba(139, 92, 246, 0.15)";
                    dropBadge.style.color = "#7c3aed";
                    dropBadge.style.border = "1px solid #c4b5fd";
                } else {
                    dropBadge.innerText = user.role || "Officer SMTI";
                    dropBadge.style.background = "rgba(2, 132, 199, 0.12)";
                    dropBadge.style.color = "#0284c7";
                    dropBadge.style.border = "1px solid #7dd3fc";
                }
            }

            // 3. Update Sidebar Footer
            const sideAvatar = document.querySelector('.sidebar-footer .user-avatar');
            const sideName = document.querySelector('.sidebar-footer .user-info .name');
            const sideRole = document.querySelector('.sidebar-footer .user-info .role');
            if (sideAvatar) {
                sideAvatar.innerText = user.initials || user.name.slice(0, 2).toUpperCase();
                sideAvatar.style.background = user.color || '#06b6d4';
            }
            if (sideName) sideName.innerText = user.name;
            if (sideRole) {
                if (user.isSuperAdmin || user.name.toLowerCase().includes('septian')) {
                    sideRole.innerHTML = `<span style="color: #38bdf8; font-weight: 700;"><i class="fas fa-shield-alt"></i> Super Admin</span>`;
                } else if (user.isManager || user.name.toLowerCase().includes('henisya')) {
                    sideRole.innerHTML = `<span style="color: #c084fc; font-weight: 700;"><i class="fas fa-crown"></i> Manager Dept SMTI</span>`;
                } else {
                    sideRole.innerText = user.role;
                }
            }

            // 4. Default author in project chat
            const chatAuthorSelect = document.getElementById('comment-author-select');
            if (chatAuthorSelect) {
                chatAuthorSelect.value = user.name;
            }

            // 5. Update batasan hak akses (Sembunyikan menu Karyawan, Anak Magang, Pengaturan, Bantuan jika bukan Super Admin)
            updateUIPermissions(user);
        }

        function updateUIPermissions(user) {
            const isSuperAdmin = user && (user.isSuperAdmin || (user.name && user.name.toLowerCase().includes('septian')));

            // 4 Menu yang disembunyikan untuk selain Super Admin
            const menuKaryawan = document.getElementById('menu-item-karyawan');
            const menuMagang = document.getElementById('menu-item-magang');
            const menuPengaturan = document.getElementById('menu-item-pengaturan');
            const menuBantuan = document.getElementById('menu-item-bantuan');
            const dropPengaturan = document.getElementById('drop-item-pengaturan');

            if (menuKaryawan) menuKaryawan.style.display = isSuperAdmin ? 'flex' : 'none';
            if (menuMagang) menuMagang.style.display = isSuperAdmin ? 'flex' : 'none';
            if (menuPengaturan) menuPengaturan.style.display = isSuperAdmin ? 'flex' : 'none';
            if (menuBantuan) menuBantuan.style.display = 'flex';
            if (dropPengaturan) dropPengaturan.style.display = isSuperAdmin ? 'flex' : 'none';

            // Tombol aksi khusus Super Admin
            document.querySelectorAll('.super-admin-only').forEach(el => {
                el.style.display = isSuperAdmin ? '' : 'none';
            });

            // Jika user non-super-admin sedang membuka halaman terlarang, kembalikan ke dasbor
            const activeSection = document.querySelector('.page-section.active');
            if (activeSection && !isSuperAdmin) {
                const restricted = ['karyawan', 'magang', 'pengaturan'];
                if (restricted.includes(activeSection.id)) {
                    showPage('dasbor', document.querySelector('.menu-item[onclick*="dasbor"]'));
                }
            }
        }

        function handleLogout() {
            if (confirm("Kunci layar dashboard dan ganti akun pengguna?")) {
                localStorage.removeItem('smti_auth_user');
                sessionStorage.removeItem('smti_auth_user');
                currentAuthUser = null;
                showPinOverlay();
            }
        }

        function openChangePinModal() {
            document.getElementById('change-pin-old').value = '';
            document.getElementById('change-pin-new').value = '';
            document.getElementById('change-pin-confirm').value = '';
            document.getElementById('change-pin-error').style.display = 'none';
            document.getElementById('modalChangePin').style.display = 'flex';
        }

        function closeChangePinModal() {
            document.getElementById('modalChangePin').style.display = 'none';
        }

        function saveNewPin(e) {
            e.preventDefault();
            if (!currentAuthUser) return;

            const oldPin = document.getElementById('change-pin-old').value.trim();
            const newPin = document.getElementById('change-pin-new').value.trim();
            const confirmPin = document.getElementById('change-pin-confirm').value.trim();
            const errEl = document.getElementById('change-pin-error');

            const curExpectedPin = currentAuthUser.pin || "1234";
            if (oldPin !== curExpectedPin && oldPin !== "1234") {
                errEl.innerText = "PIN saat ini tidak sesuai.";
                errEl.style.display = 'block';
                return;
            }
            if (newPin.length < 4) {
                errEl.innerText = "PIN baru minimal 4 digit angka.";
                errEl.style.display = 'block';
                return;
            }
            if (newPin !== confirmPin) {
                errEl.innerText = "Konfirmasi PIN baru tidak cocok.";
                errEl.style.display = 'block';
                return;
            }

            // Simpan PIN baru ke pengguna aktif & data karyawan
            currentAuthUser.pin = newPin;
            const emp = SMTI_EMPLOYEES.find(emp => emp.name.toLowerCase() === currentAuthUser.name.toLowerCase());
            if (emp) emp.pin = newPin;
            saveEmployeesData();

            localStorage.setItem('smti_auth_user', JSON.stringify(currentAuthUser));
            closeChangePinModal();
            alert(`Sukses! PIN keamanan untuk akun "${currentAuthUser.name}" berhasil diubah.`);
        }
    </script>
    <!-- =========================================================
         MODAL UNDANG ANGGOTA TIM KARYAWAN SMTI KE PROYEK
         ========================================================= -->
    <div id="modalInviteMember" class="modal" style="display: none; z-index: 100005;">
        <div class="modal-content" style="width: 520px; max-width: 95%;">
            <div class="modal-header">
                <h3><i class="fas fa-user-plus" style="color: #0284c7;"></i> Undang Karyawan SMTI ke Proyek</h3>
                <span class="close-modal" onclick="closeInviteMemberModal()">&times;</span>
            </div>
            <div style="padding: 16px 20px;">
                <p style="font-size: 12.5px; color: #64748b; margin-bottom: 14px;">
                    Pilih personil SMTI untuk diundang dan dilibatkan dalam tim proyek ini. Karyawan yang ter-invite dapat mengisi laporan progres, mencentang checklist, dan berdiskusi di chat proyek.
                </p>
                <div id="invite-employees-list" style="display: flex; flex-direction: column; gap: 8px; max-height: 340px; overflow-y: auto; padding-right: 4px;">
                    <!-- Rendered by JS -->
                </div>
            </div>
            <div style="padding: 12px 20px; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end;">
                <button type="button" class="btn" style="background: #0284c7;" onclick="closeInviteMemberModal()">Selesai</button>
            </div>
        </div>
    </div>
</body>
</html>
'''

with open(r'd:\Kerjaan\index.html', 'w', encoding='utf-8') as f:
    f.write(HTML_CONTENT)

print("Dashboard Dept SMTI updated with manual checklist & comments successfully!")

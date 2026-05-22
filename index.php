<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>shmunky: Join Group Chat</title>
    
    <!-- Premium Fonts: Kanit and Inter for clean aesthetic and Thai support -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Kanit:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- FontAwesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', 'Kanit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            background-color: #ffffff;
            color: #000000;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* --- 1. shmunky VIEW STYLE (EXACTLY MATCHING SCREENSHOT) --- */
        .tg-header {
            width: 100%;
            background-color: #ffffff;
            border-bottom: 1px solid #e6e6e6;
            height: 48px;
            display: flex;
            align-items: center;
            padding: 0 5%;
        }

        .tg-logo-container {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: #000000;
        }

        .tg-logo-icon {
            width: 28px;
            height: 28px;
            background-color: #2ca5e0;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 15px;
        }

        .tg-logo-text {
            font-size: 18px;
            font-weight: 600;
            letter-spacing: -0.5px;
        }

        /* Notice Banner */
        .tg-notice-banner {
            width: 100%;
            background-color: #33a1e4;
            color: #ffffff;
            text-align: center;
            padding: 10px 15px;
            font-size: 13.5px;
            font-weight: 400;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .tg-notice-banner:hover {
            background-color: #2ca5e0;
        }

        /* Main Content Grid */
        .tg-main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding-top: 60px;
            padding-left: 20px;
            padding-right: 20px;
            text-align: center;
            max-width: 620px;
            margin: 0 auto;
            width: 100%;
        }

        /* Avatar Container */
        .avatar-wrapper {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            overflow: hidden;
            background: linear-gradient(135deg, #2ea6ff 0%, #1a73e8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            font-size: 42px;
            font-weight: 600;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            position: relative;
        }

        .avatar-wrapper img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
        }

        /* Titles and stats styling */
        .group-title {
            font-size: 22px;
            font-weight: 600;
            color: #000000;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }

        .group-title i.verified-badge {
            color: #2ca5e0;
            font-size: 18px;
        }

        .group-stats {
            font-size: 14px;
            color: #8a8a8a;
            margin-bottom: 12px;
            font-weight: 400;
        }

        .group-description {
            font-size: 15px;
            color: #333333;
            line-height: 1.6;
            margin-bottom: 25px;
            word-break: break-word;
            max-width: 480px;
        }

        /* Button Styling - Vibrant Green matching user screenshot */
        .btn-view-tg {
            background-color: #24d366; /* Vibrant Emerald/Mint Green */
            color: #ffffff;
            text-decoration: none;
            font-size: 13.5px;
            font-weight: 600;
            text-transform: uppercase;
            padding: 12px 36px;
            border-radius: 30px;
            display: inline-block;
            transition: background-color 0.2s, transform 0.1s;
            border: none;
            cursor: pointer;
            letter-spacing: 0.5px;
        }

        .btn-view-tg:hover {
            background-color: #1ebe5d;
        }

        .btn-view-tg:active {
            transform: scale(0.97);
        }


        
    });
</script>

</body>
</html>

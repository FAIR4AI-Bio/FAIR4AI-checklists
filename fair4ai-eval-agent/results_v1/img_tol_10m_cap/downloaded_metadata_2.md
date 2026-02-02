<!doctype html>
<html class="">
	<head>
		<meta charset="utf-8" />

		<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />

		<meta name="description" content="We’re on a journey to advance and democratize artificial intelligence through open source and open science." />

		<meta property="fb:app_id" content="1321688464574422" />

		<meta name="twitter:card" content="summary_large_image" />

		<meta name="twitter:site" content="@huggingface" />

		<meta name="twitter:image" content="https://cdn-thumbnails.huggingface.co/social-thumbnails/models/imageomics/biocap.png" />

		<meta property="og:title" content="README.md · imageomics/biocap at main" />

		<meta property="og:description" content="We’re on a journey to advance and democratize artificial intelligence through open source and open science." />

		<meta property="og:type" content="website" />

		<meta property="og:url" content="https://huggingface.co/imageomics/biocap/blob/main/README.md" />

		<meta property="og:image" content="https://cdn-thumbnails.huggingface.co/social-thumbnails/models/imageomics/biocap.png" />

		<link rel="stylesheet" href="/front/build/kube-08e8472/style.css" />

		<link rel="preconnect" href="https://fonts.gstatic.com" />

		<link
			href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:ital,wght@0,200;0,300;0,400;0,600;0,700;1,200;1,300;1,400;1,600;1,700&display=swap"
			rel="stylesheet"
		/>

		<link
			href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&display=swap"
			rel="stylesheet"
		/>

		<link
			rel="preload"
			href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.12.0/katex.min.css"
			as="style"
			onload="
				this.onload = null;
				this.rel = 'stylesheet';
			"
		/>

		<noscript>
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.12.0/katex.min.css" />
		</noscript>
		<script>const guestTheme = document.cookie.match(/theme=(\w+)/)?.[1]; document.documentElement.classList.toggle('dark', guestTheme === 'dark' || ( (!guestTheme || guestTheme === 'system') && window.matchMedia('(prefers-color-scheme: dark)').matches));</script>
<link rel="canonical" href="https://huggingface.co/imageomics/biocap/blob/main/README.md">  
		<title>README.md · imageomics/biocap at main</title>

		<script defer src="/js/script.js"></script>

		<script>
			((window.plausible =
				window.plausible
				|| function () {
					(plausible.q = plausible.q || []).push(arguments);
				}),
				(plausible.init =
					plausible.init
					|| function (i) {
						plausible.o = i || {};
					}));
			plausible.init({
				customProperties: {
					loggedIn: "false",
				},
				endpoint: "/api/event",
			});
		</script>

		<script>
			window.hubConfig = {"features":{"signupDisabled":false},"sshGitUrl":"git@hf.co","moonHttpUrl":"https:\/\/huggingface.co","captchaApiKey":"bd5f2066-93dc-4bdd-a64b-a24646ca3859","datasetViewerPublicUrl":"https:\/\/datasets-server.huggingface.co","stripePublicKey":"pk_live_x2tdjFXBCvXo2FFmMybezpeM00J6gPCAAc","environment":"production","userAgent":"HuggingFace (production)","spacesIframeDomain":"hf.space","spacesApiUrl":"https:\/\/api.hf.space","docSearchKey":"ece5e02e57300e17d152c08056145326e90c4bff3dd07d7d1ae40cf1c8d39cb6","logoDev":{"apiUrl":"https:\/\/img.logo.dev\/","apiKey":"pk_UHS2HZOeRnaSOdDp7jbd5w"}};
			window.requestId = "Root=1-698034cf-00fb07e87aaeef15164dd8c8";
		</script>
		<script type="text/javascript" src="https://de5282c3ca0c.edge.sdk.awswaf.com/de5282c3ca0c/526cf06acb0d/challenge.js" defer></script> 
	</head>
	<body class="flex flex-col min-h-dvh bg-white dark:bg-gray-950 text-black ViewerBlobPage">
		<div class="flex min-h-dvh flex-col"><div class="SVELTE_HYDRATER contents" data-target="DeviceProvider" data-props="{}"></div>
	<div class="SVELTE_HYDRATER contents" data-target="SystemThemeMonitor" data-props="{&quot;isLoggedIn&quot;:false}"></div>

	<div class="SVELTE_HYDRATER contents" data-target="MainHeader" data-props="{&quot;classNames&quot;:&quot;&quot;,&quot;isWide&quot;:false,&quot;isZh&quot;:false,&quot;isPro&quot;:false}"><header class="border-b border-gray-100 "><div class="w-full px-4 container flex h-16 items-center"><div class="flex flex-1 items-center"><a class="mr-5 flex flex-none items-center lg:mr-6" href="/"><img alt="Hugging Face's logo" class="w-7 md:mr-2" src="/front/assets/huggingface_logo-noborder.svg">
				<span class="hidden whitespace-nowrap text-lg font-bold md:block">Hugging Face</span></a>
			<div class="relative flex-1 lg:max-w-sm mr-2 sm:mr-4 md:mr-3 xl:mr-6"><input autocomplete="off" class="w-full dark:bg-gray-950 pl-8 form-input-alt h-9 pr-3 focus:shadow-xl " name="" placeholder="Search models, datasets, users..."   spellcheck="false" type="text" value="">
	<svg class="absolute left-2.5 text-gray-400 top-1/2 transform -translate-y-1/2" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M30 28.59L22.45 21A11 11 0 1 0 21 22.45L28.59 30zM5 14a9 9 0 1 1 9 9a9 9 0 0 1-9-9z" fill="currentColor"></path></svg>
	</div>
			<div class="flex flex-none items-center justify-center p-0.5 place-self-stretch lg:hidden"><button class="relative z-40 flex h-6 w-8 items-center justify-center" type="button"><svg width="1em" height="1em" viewBox="0 0 10 10" class="text-xl" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" preserveAspectRatio="xMidYMid meet" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.65039 2.9999C1.65039 2.8066 1.80709 2.6499 2.00039 2.6499H8.00039C8.19369 2.6499 8.35039 2.8066 8.35039 2.9999C8.35039 3.1932 8.19369 3.3499 8.00039 3.3499H2.00039C1.80709 3.3499 1.65039 3.1932 1.65039 2.9999ZM1.65039 4.9999C1.65039 4.8066 1.80709 4.6499 2.00039 4.6499H8.00039C8.19369 4.6499 8.35039 4.8066 8.35039 4.9999C8.35039 5.1932 8.19369 5.3499 8.00039 5.3499H2.00039C1.80709 5.3499 1.65039 5.1932 1.65039 4.9999ZM2.00039 6.6499C1.80709 6.6499 1.65039 6.8066 1.65039 6.9999C1.65039 7.1932 1.80709 7.3499 2.00039 7.3499H8.00039C8.19369 7.3499 8.35039 7.1932 8.35039 6.9999C8.35039 6.8066 8.19369 6.6499 8.00039 6.6499H2.00039Z"></path></svg>
		</button>

	</div></div>
		<nav aria-label="Main" class="ml-auto hidden lg:block"><ul class="flex items-center gap-x-1 2xl:gap-x-2"><li class="hover:text-indigo-700"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/models"><svg class="mr-1.5 text-gray-400 group-hover:text-indigo-500" style="" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path class="uim-quaternary" d="M20.23 7.24L12 12L3.77 7.24a1.98 1.98 0 0 1 .7-.71L11 2.76c.62-.35 1.38-.35 2 0l6.53 3.77c.29.173.531.418.7.71z" opacity=".25" fill="currentColor"></path><path class="uim-tertiary" d="M12 12v9.5a2.09 2.09 0 0 1-.91-.21L4.5 17.48a2.003 2.003 0 0 1-1-1.73v-7.5a2.06 2.06 0 0 1 .27-1.01L12 12z" opacity=".5" fill="currentColor"></path><path class="uim-primary" d="M20.5 8.25v7.5a2.003 2.003 0 0 1-1 1.73l-6.62 3.82c-.275.13-.576.198-.88.2V12l8.23-4.76c.175.308.268.656.27 1.01z" fill="currentColor"></path></svg>
						Models</a>
				</li><li class="hover:text-red-700"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/datasets"><svg class="mr-1.5 text-gray-400 group-hover:text-red-500" style="" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 25 25"><ellipse cx="12.5" cy="5" fill="currentColor" fill-opacity="0.25" rx="7.5" ry="2"></ellipse><path d="M12.5 15C16.6421 15 20 14.1046 20 13V20C20 21.1046 16.6421 22 12.5 22C8.35786 22 5 21.1046 5 20V13C5 14.1046 8.35786 15 12.5 15Z" fill="currentColor" opacity="0.5"></path><path d="M12.5 7C16.6421 7 20 6.10457 20 5V11.5C20 12.6046 16.6421 13.5 12.5 13.5C8.35786 13.5 5 12.6046 5 11.5V5C5 6.10457 8.35786 7 12.5 7Z" fill="currentColor" opacity="0.5"></path><path d="M5.23628 12C5.08204 12.1598 5 12.8273 5 13C5 14.1046 8.35786 15 12.5 15C16.6421 15 20 14.1046 20 13C20 12.8273 19.918 12.1598 19.7637 12C18.9311 12.8626 15.9947 13.5 12.5 13.5C9.0053 13.5 6.06886 12.8626 5.23628 12Z" fill="currentColor"></path></svg>
						Datasets</a>
				</li><li class="hover:text-blue-700"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/spaces"><svg class="mr-1.5 text-gray-400 group-hover:text-blue-500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" viewBox="0 0 25 25"><path opacity=".5" d="M6.016 14.674v4.31h4.31v-4.31h-4.31ZM14.674 14.674v4.31h4.31v-4.31h-4.31ZM6.016 6.016v4.31h4.31v-4.31h-4.31Z" fill="currentColor"></path><path opacity=".75" fill-rule="evenodd" clip-rule="evenodd" d="M3 4.914C3 3.857 3.857 3 4.914 3h6.514c.884 0 1.628.6 1.848 1.414a5.171 5.171 0 0 1 7.31 7.31c.815.22 1.414.964 1.414 1.848v6.514A1.914 1.914 0 0 1 20.086 22H4.914A1.914 1.914 0 0 1 3 20.086V4.914Zm3.016 1.102v4.31h4.31v-4.31h-4.31Zm0 12.968v-4.31h4.31v4.31h-4.31Zm8.658 0v-4.31h4.31v4.31h-4.31Zm0-10.813a2.155 2.155 0 1 1 4.31 0 2.155 2.155 0 0 1-4.31 0Z" fill="currentColor"></path><path opacity=".25" d="M16.829 6.016a2.155 2.155 0 1 0 0 4.31 2.155 2.155 0 0 0 0-4.31Z" fill="currentColor"></path></svg>
						Spaces</a>
				</li><li class="max-xl:hidden relative"><div class="relative ">
	<button class="group flex items-center px-2 py-0.5 dark:text-gray-300 hover:text-yellow-700 dark:hover:text-gray-100 " type="button">
		<svg class="mr-1.5 mr-1.5 text-gray-400 text-yellow-500! group-hover:text-yellow-500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M20.6081 3C21.7684 3 22.8053 3.49196 23.5284 4.38415C23.9756 4.93678 24.4428 5.82749 24.4808 7.16133C24.9674 7.01707 25.4353 6.93643 25.8725 6.93643C26.9833 6.93643 27.9865 7.37587 28.696 8.17411C29.6075 9.19872 30.0124 10.4579 29.8361 11.7177C29.7523 12.3177 29.5581 12.8555 29.2678 13.3534C29.8798 13.8646 30.3306 14.5763 30.5485 15.4322C30.719 16.1032 30.8939 17.5006 29.9808 18.9403C30.0389 19.0342 30.0934 19.1319 30.1442 19.2318C30.6932 20.3074 30.7283 21.5229 30.2439 22.6548C29.5093 24.3704 27.6841 25.7219 24.1397 27.1727C21.9347 28.0753 19.9174 28.6523 19.8994 28.6575C16.9842 29.4379 14.3477 29.8345 12.0653 29.8345C7.87017 29.8345 4.8668 28.508 3.13831 25.8921C0.356375 21.6797 0.754104 17.8269 4.35369 14.1131C6.34591 12.058 7.67023 9.02782 7.94613 8.36275C8.50224 6.39343 9.97271 4.20438 12.4172 4.20438H12.4179C12.6236 4.20438 12.8314 4.2214 13.0364 4.25468C14.107 4.42854 15.0428 5.06476 15.7115 6.02205C16.4331 5.09583 17.134 4.359 17.7682 3.94323C18.7242 3.31737 19.6794 3 20.6081 3ZM20.6081 5.95917C20.2427 5.95917 19.7963 6.1197 19.3039 6.44225C17.7754 7.44319 14.8258 12.6772 13.7458 14.7131C13.3839 15.3952 12.7655 15.6837 12.2086 15.6837C11.1036 15.6837 10.2408 14.5497 12.1076 13.1085C14.9146 10.9402 13.9299 7.39584 12.5898 7.1776C12.5311 7.16799 12.4731 7.16355 12.4172 7.16355C11.1989 7.16355 10.6615 9.33114 10.6615 9.33114C10.6615 9.33114 9.0863 13.4148 6.38031 16.206C3.67434 18.998 3.5346 21.2388 5.50675 24.2246C6.85185 26.2606 9.42666 26.8753 12.0653 26.8753C14.8021 26.8753 17.6077 26.2139 19.1799 25.793C19.2574 25.7723 28.8193 22.984 27.6081 20.6107C27.4046 20.212 27.0693 20.0522 26.6471 20.0522C24.9416 20.0522 21.8393 22.6726 20.5057 22.6726C20.2076 22.6726 19.9976 22.5416 19.9116 22.222C19.3433 20.1173 28.552 19.2325 27.7758 16.1839C27.639 15.6445 27.2677 15.4256 26.746 15.4263C24.4923 15.4263 19.4358 19.5181 18.3759 19.5181C18.2949 19.5181 18.2368 19.4937 18.2053 19.4419C17.6743 18.557 17.9653 17.9394 21.7082 15.6009C25.4511 13.2617 28.0783 11.8545 26.5841 10.1752C26.4121 9.98141 26.1684 9.8956 25.8725 9.8956C23.6001 9.89634 18.2311 14.9403 18.2311 14.9403C18.2311 14.9403 16.7821 16.496 15.9057 16.496C15.7043 16.496 15.533 16.4139 15.4169 16.2112C14.7956 15.1296 21.1879 10.1286 21.5484 8.06535C21.7928 6.66715 21.3771 5.95917 20.6081 5.95917Z" fill="#FF9D00"></path><path d="M5.50686 24.2246C3.53472 21.2387 3.67446 18.9979 6.38043 16.206C9.08641 13.4147 10.6615 9.33111 10.6615 9.33111C10.6615 9.33111 11.2499 6.95933 12.59 7.17757C13.93 7.39581 14.9139 10.9401 12.1069 13.1084C9.29997 15.276 12.6659 16.7489 13.7459 14.713C14.8258 12.6772 17.7747 7.44316 19.304 6.44221C20.8326 5.44128 21.9089 6.00204 21.5484 8.06532C21.188 10.1286 14.795 15.1295 15.4171 16.2118C16.0391 17.2934 18.2312 14.9402 18.2312 14.9402C18.2312 14.9402 25.0907 8.49588 26.5842 10.1752C28.0776 11.8545 25.4512 13.2616 21.7082 15.6008C17.9646 17.9393 17.6744 18.557 18.2054 19.4418C18.7372 20.3266 26.9998 13.1351 27.7759 16.1838C28.5513 19.2324 19.3434 20.1173 19.9117 22.2219C20.48 24.3274 26.3979 18.2382 27.6082 20.6107C28.8193 22.9839 19.2574 25.7722 19.18 25.7929C16.0914 26.62 8.24723 28.3726 5.50686 24.2246Z" fill="#FFD21E"></path></svg>
			Community
		</button>
	
	
	</div>
				</li><li class="hover:text-yellow-700"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/docs"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="mr-1.5 text-gray-400 group-hover:text-yellow-500" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 16 16"><path d="m2.28 3.7-.3.16a.67.67 0 0 0-.34.58v8.73l.01.04.02.07.01.04.03.06.02.04.02.03.04.06.05.05.04.04.06.04.06.04.08.04.08.02h.05l.07.02h.11l.04-.01.07-.02.03-.01.07-.03.22-.12a5.33 5.33 0 0 1 5.15.1.67.67 0 0 0 .66 0 5.33 5.33 0 0 1 5.33 0 .67.67 0 0 0 1-.58V4.36a.67.67 0 0 0-.34-.5l-.3-.17v7.78a.63.63 0 0 1-.87.59 4.9 4.9 0 0 0-4.35.35l-.65.39a.29.29 0 0 1-.15.04.29.29 0 0 1-.16-.04l-.65-.4a4.9 4.9 0 0 0-4.34-.34.63.63 0 0 1-.87-.59V3.7Z" fill="currentColor" class="dark:opacity-40"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M8 3.1a5.99 5.99 0 0 0-5.3-.43.66.66 0 0 0-.42.62v8.18c0 .45.46.76.87.59a4.9 4.9 0 0 1 4.34.35l.65.39c.05.03.1.04.16.04.05 0 .1-.01.15-.04l.65-.4a4.9 4.9 0 0 1 4.35-.34.63.63 0 0 0 .86-.59V3.3a.67.67 0 0 0-.41-.62 5.99 5.99 0 0 0-5.3.43l-.3.17L8 3.1Zm.73 1.87a.43.43 0 1 0-.86 0v5.48a.43.43 0 0 0 .86 0V4.97Z" fill="currentColor" class="opacity-40 dark:opacity-100"></path><path d="M8.73 4.97a.43.43 0 1 0-.86 0v5.48a.43.43 0 1 0 .86 0V4.96Z" fill="currentColor" class="dark:opacity-40"></path></svg>
						Docs</a>
				</li><li class="hover:text-black dark:hover:text-white max-2xl:hidden"><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/enterprise"><svg class="mr-1.5 text-gray-400 group-hover:text-black dark:group-hover:text-white" xmlns="http://www.w3.org/2000/svg" fill="none" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 12 12"><path fill-rule="evenodd" clip-rule="evenodd" d="M4.9 1.35a3.16 3.16 0 0 0-2.8 2.07L.37 8.58C0 9.71.7 10.65 1.86 10.65H7.3a3.2 3.2 0 0 0 2.84-2.07l1.67-5.16c.36-1.13-.3-2.07-1.46-2.07H4.91Zm.4 2.07L3.57 8.47h3.57l.36-1.12H5.4l.28-.91h1.75l.4-1.1H6.07l.3-.83h2l.36-1.1H5.27h.04Z" fill="currentColor"></path></svg>
						Enterprise</a>
				</li>

		<li><a class="group flex items-center px-2 py-0.5 dark:text-gray-300 dark:hover:text-gray-100" href="/pricing">Pricing
			</a></li>

		<li><div class="relative group">
	<button class="px-2 py-0.5 hover:text-gray-500 dark:hover:text-gray-600 flex items-center " type="button">
		<svg class=" text-gray-500 w-5 group-hover:text-gray-400 dark:text-gray-300 dark:group-hover:text-gray-100" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" viewBox="0 0 32 18" preserveAspectRatio="xMidYMid meet"><path fill-rule="evenodd" clip-rule="evenodd" d="M14.4504 3.30221C14.4504 2.836 14.8284 2.45807 15.2946 2.45807H28.4933C28.9595 2.45807 29.3374 2.836 29.3374 3.30221C29.3374 3.76842 28.9595 4.14635 28.4933 4.14635H15.2946C14.8284 4.14635 14.4504 3.76842 14.4504 3.30221Z" fill="currentColor"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M14.4504 9.00002C14.4504 8.53382 14.8284 8.15588 15.2946 8.15588H28.4933C28.9595 8.15588 29.3374 8.53382 29.3374 9.00002C29.3374 9.46623 28.9595 9.84417 28.4933 9.84417H15.2946C14.8284 9.84417 14.4504 9.46623 14.4504 9.00002Z" fill="currentColor"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M14.4504 14.6978C14.4504 14.2316 14.8284 13.8537 15.2946 13.8537H28.4933C28.9595 13.8537 29.3374 14.2316 29.3374 14.6978C29.3374 15.164 28.9595 15.542 28.4933 15.542H15.2946C14.8284 15.542 14.4504 15.164 14.4504 14.6978Z" fill="currentColor"></path><path fill-rule="evenodd" clip-rule="evenodd" d="M1.94549 6.87377C2.27514 6.54411 2.80962 6.54411 3.13928 6.87377L6.23458 9.96907L9.32988 6.87377C9.65954 6.54411 10.194 6.54411 10.5237 6.87377C10.8533 7.20343 10.8533 7.73791 10.5237 8.06756L6.23458 12.3567L1.94549 8.06756C1.61583 7.73791 1.61583 7.20343 1.94549 6.87377Z" fill="currentColor"></path></svg>
			
		</button>
	
	
	</div></li>
		<li><hr class="h-5 w-0.5 border-none bg-gray-100 dark:bg-gray-800"></li>
		<li><a class="block cursor-pointer whitespace-nowrap px-2 py-0.5 hover:text-gray-500 dark:text-gray-300 dark:hover:text-gray-100" href="/login">Log In
				</a></li>
			<li><a class="whitespace-nowrap rounded-full border border-transparent bg-gray-900 px-3 py-1 leading-none text-white hover:border-black hover:bg-white hover:text-black" href="/join">Sign Up
					</a></li></ul></nav></div></header></div>
	
	
	
	<div class="SVELTE_HYDRATER contents" data-target="SSOBanner" data-props="{}"></div>
	

	<main class="flex flex-1 flex-col">
	<div class="SVELTE_HYDRATER contents" data-target="ModelHeader" data-props="{&quot;activeTab&quot;:&quot;files&quot;,&quot;author&quot;:{&quot;_id&quot;:&quot;6330c5f48ef21f473089e0c4&quot;,&quot;avatarUrl&quot;:&quot;https://cdn-avatars.huggingface.co/v1/production/uploads/1664140778418-6330c479c375586dc3b2aa2c.jpeg&quot;,&quot;fullname&quot;:&quot;HDR Imageomics Institute&quot;,&quot;name&quot;:&quot;imageomics&quot;,&quot;type&quot;:&quot;org&quot;,&quot;isHf&quot;:false,&quot;isHfAdmin&quot;:false,&quot;isMod&quot;:false,&quot;followerCount&quot;:148,&quot;isUserFollowing&quot;:false},&quot;canReadRepoSettings&quot;:false,&quot;canWriteRepoContent&quot;:false,&quot;canDisable&quot;:false,&quot;model&quot;:{&quot;author&quot;:&quot;imageomics&quot;,&quot;cardData&quot;:{&quot;license&quot;:[&quot;mit&quot;],&quot;language&quot;:[&quot;en&quot;],&quot;library_name&quot;:&quot;open_clip&quot;,&quot;model_name&quot;:&quot;BioCAP&quot;,&quot;model_description&quot;:&quot;Foundation model for biology organismal images. It is trained on TreeOfLife-10M with synthetic captions (TreeOfLife-10M-Captions) as supervision on the basis of a CLIP model (ViT-B/16) pre-trained by openai. BioCAP achieves state-of-the-art performance on text-image retrieval tasks.&quot;,&quot;tags&quot;:[&quot;biology&quot;,&quot;CV&quot;,&quot;images&quot;,&quot;imageomics&quot;,&quot;clip&quot;,&quot;species-classification&quot;,&quot;biological visual task&quot;,&quot;multimodal&quot;,&quot;animals&quot;,&quot;plants&quot;,&quot;fungi&quot;,&quot;species&quot;,&quot;taxonomy&quot;,&quot;rare species&quot;,&quot;endangered species&quot;,&quot;evolutionary biology&quot;,&quot;knowledge-guided&quot;,&quot;zero-shot-image-classification&quot;,&quot;zero-shot-text-retrieval&quot;],&quot;datasets&quot;:[&quot;imageomics/TreeOfLife-10M-Captions&quot;,&quot;imageomics/TreeOfLife-10M&quot;,&quot;iNat21&quot;,&quot;BIOSCAN-1M&quot;,&quot;EOL&quot;]},&quot;cardExists&quot;:true,&quot;config&quot;:{&quot;tokenizer_config&quot;:{&quot;bos_token&quot;:{&quot;__type&quot;:&quot;AddedToken&quot;,&quot;content&quot;:&quot;<|startoftext|>&quot;,&quot;lstrip&quot;:false,&quot;normalized&quot;:true,&quot;rstrip&quot;:false,&quot;single_word&quot;:false},&quot;eos_token&quot;:{&quot;__type&quot;:&quot;AddedToken&quot;,&quot;content&quot;:&quot;<|endoftext|>&quot;,&quot;lstrip&quot;:false,&quot;normalized&quot;:true,&quot;rstrip&quot;:false,&quot;single_word&quot;:false},&quot;pad_token&quot;:&quot;<|endoftext|>&quot;,&quot;unk_token&quot;:{&quot;__type&quot;:&quot;AddedToken&quot;,&quot;content&quot;:&quot;<|endoftext|>&quot;,&quot;lstrip&quot;:false,&quot;normalized&quot;:true,&quot;rstrip&quot;:false,&quot;single_word&quot;:false}}},&quot;createdAt&quot;:&quot;2025-10-08T06:47:52.000Z&quot;,&quot;discussionsDisabled&quot;:false,&quot;discussionsSorting&quot;:&quot;recently-created&quot;,&quot;downloads&quot;:122,&quot;downloadsAllTime&quot;:407,&quot;doi&quot;:{&quot;id&quot;:&quot;10.57967/hf/6799&quot;,&quot;commit&quot;:&quot;af8db7ab8965a2769c8613cfe8bfaf2f4d9de1b5&quot;,&quot;customAuthors&quot;:[{&quot;name&quot;:&quot;Ziheng Zhang&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Xinyue Ma&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Arpita Chowdhury&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Elizabeth G Campolongo&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Matthew J Thompson&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Net Zhang&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Samuel Stevens&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Hilmar Lapp&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Tanya Berger-Wolf&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Yu Su&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Wei-Lun Chao&quot;,&quot;nameType&quot;:&quot;Personal&quot;},{&quot;name&quot;:&quot;Jianyang Gu&quot;,&quot;nameType&quot;:&quot;Personal&quot;}]},&quot;id&quot;:&quot;imageomics/biocap&quot;,&quot;isLikedByUser&quot;:false,&quot;availableInferenceProviders&quot;:[],&quot;inference&quot;:&quot;&quot;,&quot;lastModified&quot;:&quot;2025-10-24T13:56:09.000Z&quot;,&quot;likes&quot;:0,&quot;pipeline_tag&quot;:&quot;zero-shot-image-classification&quot;,&quot;library_name&quot;:&quot;open_clip&quot;,&quot;librariesOther&quot;:[],&quot;trackDownloads&quot;:true,&quot;model-index&quot;:null,&quot;private&quot;:false,&quot;repoType&quot;:&quot;model&quot;,&quot;gated&quot;:false,&quot;tags&quot;:[&quot;open_clip&quot;,&quot;safetensors&quot;,&quot;biology&quot;,&quot;CV&quot;,&quot;images&quot;,&quot;imageomics&quot;,&quot;clip&quot;,&quot;species-classification&quot;,&quot;biological visual task&quot;,&quot;multimodal&quot;,&quot;animals&quot;,&quot;plants&quot;,&quot;fungi&quot;,&quot;species&quot;,&quot;taxonomy&quot;,&quot;rare species&quot;,&quot;endangered species&quot;,&quot;evolutionary biology&quot;,&quot;knowledge-guided&quot;,&quot;zero-shot-image-classification&quot;,&quot;zero-shot-text-retrieval&quot;,&quot;en&quot;,&quot;dataset:imageomics/TreeOfLife-10M-Captions&quot;,&quot;dataset:imageomics/TreeOfLife-10M&quot;,&quot;dataset:iNat21&quot;,&quot;dataset:BIOSCAN-1M&quot;,&quot;dataset:EOL&quot;,&quot;arxiv:2510.20095&quot;,&quot;doi:10.57967/hf/6799&quot;,&quot;license:mit&quot;,&quot;region:us&quot;],&quot;tag_objs&quot;:[{&quot;id&quot;:&quot;zero-shot-image-classification&quot;,&quot;label&quot;:&quot;Zero-Shot Image Classification&quot;,&quot;type&quot;:&quot;pipeline_tag&quot;,&quot;subType&quot;:&quot;cv&quot;},{&quot;id&quot;:&quot;open_clip&quot;,&quot;label&quot;:&quot;OpenCLIP&quot;,&quot;type&quot;:&quot;library&quot;},{&quot;id&quot;:&quot;safetensors&quot;,&quot;label&quot;:&quot;Safetensors&quot;,&quot;type&quot;:&quot;library&quot;},{&quot;id&quot;:&quot;dataset:imageomics/TreeOfLife-10M-Captions&quot;,&quot;label&quot;:&quot;imageomics/TreeOfLife-10M-Captions&quot;,&quot;type&quot;:&quot;dataset&quot;,&quot;extra&quot;:{&quot;disabled&quot;:false}},{&quot;id&quot;:&quot;dataset:imageomics/TreeOfLife-10M&quot;,&quot;label&quot;:&quot;imageomics/TreeOfLife-10M&quot;,&quot;type&quot;:&quot;dataset&quot;,&quot;extra&quot;:{&quot;disabled&quot;:false}},{&quot;id&quot;:&quot;dataset:iNat21&quot;,&quot;label&quot;:&quot;iNat21&quot;,&quot;type&quot;:&quot;dataset&quot;,&quot;extra&quot;:{&quot;disabled&quot;:true}},{&quot;id&quot;:&quot;dataset:BIOSCAN-1M&quot;,&quot;label&quot;:&quot;BIOSCAN-1M&quot;,&quot;type&quot;:&quot;dataset&quot;,&quot;extra&quot;:{&quot;disabled&quot;:true}},{&quot;id&quot;:&quot;dataset:EOL&quot;,&quot;label&quot;:&quot;EOL&quot;,&quot;type&quot;:&quot;dataset&quot;,&quot;extra&quot;:{&quot;disabled&quot;:true}},{&quot;id&quot;:&quot;en&quot;,&quot;label&quot;:&quot;English&quot;,&quot;type&quot;:&quot;language&quot;},{&quot;id&quot;:&quot;doi:10.57967/hf/6799&quot;,&quot;label&quot;:&quot;doi:10.57967/hf/6799&quot;,&quot;type&quot;:&quot;doi&quot;},{&quot;id&quot;:&quot;biology&quot;,&quot;label&quot;:&quot;biology&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;CV&quot;,&quot;label&quot;:&quot;CV&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;images&quot;,&quot;label&quot;:&quot;images&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;imageomics&quot;,&quot;label&quot;:&quot;imageomics&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;clip&quot;,&quot;label&quot;:&quot;clip&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;species-classification&quot;,&quot;label&quot;:&quot;species-classification&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;biological visual task&quot;,&quot;label&quot;:&quot;biological visual task&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;multimodal&quot;,&quot;label&quot;:&quot;multimodal&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;animals&quot;,&quot;label&quot;:&quot;animals&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;plants&quot;,&quot;label&quot;:&quot;plants&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;fungi&quot;,&quot;label&quot;:&quot;fungi&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;species&quot;,&quot;label&quot;:&quot;species&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;taxonomy&quot;,&quot;label&quot;:&quot;taxonomy&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;rare species&quot;,&quot;label&quot;:&quot;rare species&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;endangered species&quot;,&quot;label&quot;:&quot;endangered species&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;evolutionary biology&quot;,&quot;label&quot;:&quot;evolutionary biology&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;knowledge-guided&quot;,&quot;label&quot;:&quot;knowledge-guided&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;zero-shot-text-retrieval&quot;,&quot;label&quot;:&quot;zero-shot-text-retrieval&quot;,&quot;type&quot;:&quot;other&quot;,&quot;clickable&quot;:true},{&quot;id&quot;:&quot;arxiv:2510.20095&quot;,&quot;label&quot;:&quot;arxiv:2510.20095&quot;,&quot;type&quot;:&quot;arxiv&quot;,&quot;extra&quot;:{&quot;paperTitle&quot;:&quot;BIOCAP: Exploiting Synthetic Captions Beyond Labels in Biological\n  Foundation Models&quot;}},{&quot;id&quot;:&quot;license:mit&quot;,&quot;label&quot;:&quot;mit&quot;,&quot;type&quot;:&quot;license&quot;},{&quot;type&quot;:&quot;region&quot;,&quot;label&quot;:&quot;🇺🇸 Region: US&quot;,&quot;id&quot;:&quot;region:us&quot;}],&quot;hasBlockedOids&quot;:false,&quot;region&quot;:&quot;us&quot;,&quot;isQuantized&quot;:false},&quot;discussionsStats&quot;:{&quot;closed&quot;:0,&quot;open&quot;:0,&quot;total&quot;:0},&quot;query&quot;:{},&quot;inferenceContextData&quot;:{&quot;billableEntities&quot;:[],&quot;entityName2Providers&quot;:{}}}">
<header class="bg-linear-to-t border-b border-gray-100 pt-6 sm:pt-9 from-gray-50-to-white via-white dark:via-gray-950"><div class="container relative "><h1 class="flex flex-wrap items-center max-md:leading-tight mb-3 text-lg max-sm:gap-y-1.5 md:text-xl">
			<div class="group flex flex-none items-center"><div class="relative mr-1 flex items-center">

			

<span class="inline-block "><span class="contents"><a href="/imageomics" class="text-gray-400 hover:text-blue-600"><div class="flex-none  "><img alt="" class="size-3.5 rounded-sm  flex-none select-none" src="https://cdn-avatars.huggingface.co/v1/production/uploads/1664140778418-6330c479c375586dc3b2aa2c.jpeg" crossorigin="anonymous">
	</div></a></span>
	</span></div>
		

<span class="inline-block "><span class="contents"><a href="/imageomics" class="text-gray-400 hover:text-blue-600">imageomics</a></span>
	</span>
		<div class="mx-0.5 text-gray-300">/</div></div>

<div class="max-w-full "><a class="break-words font-mono font-semibold hover:text-blue-600 " href="/imageomics/biocap">biocap</a>
	<button class="text-sm mr-4 focus:outline-hidden inline-flex cursor-pointer items-center text-sm  mx-0.5   text-gray-600 " title="Copy model name to clipboard" type="button"><svg class="" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="currentColor" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M28,10V28H10V10H28m0-2H10a2,2,0,0,0-2,2V28a2,2,0,0,0,2,2H28a2,2,0,0,0,2-2V10a2,2,0,0,0-2-2Z" transform="translate(0)"></path><path d="M4,18H2V4A2,2,0,0,1,4,2H18V4H4Z" transform="translate(0)"></path><rect fill="none" width="32" height="32"></rect></svg>
		</button></div>
			<div class="inline-flex items-center overflow-hidden whitespace-nowrap rounded-md border bg-white text-sm leading-none text-gray-500  mr-2"><button class="relative flex items-center overflow-hidden from-red-50 to-transparent dark:from-red-900 px-1.5 py-1 hover:bg-linear-to-t focus:outline-hidden"  title="Like"><svg class="left-1.5 absolute" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32" fill="currentColor"><path d="M22.45,6a5.47,5.47,0,0,1,3.91,1.64,5.7,5.7,0,0,1,0,8L16,26.13,5.64,15.64a5.7,5.7,0,0,1,0-8,5.48,5.48,0,0,1,7.82,0L16,10.24l2.53-2.58A5.44,5.44,0,0,1,22.45,6m0-2a7.47,7.47,0,0,0-5.34,2.24L16,7.36,14.89,6.24a7.49,7.49,0,0,0-10.68,0,7.72,7.72,0,0,0,0,10.82L16,29,27.79,17.06a7.72,7.72,0,0,0,0-10.82A7.49,7.49,0,0,0,22.45,4Z"></path></svg>

		
		<span class="ml-4 pl-0.5 ">like</span></button>
	<button class="focus:outline-hidden flex items-center border-l px-1.5 py-1 text-gray-400 hover:bg-gray-50 focus:bg-gray-100 dark:hover:bg-gray-900 dark:focus:bg-gray-800" title="See users who liked this repository">0</button></div>


			<div class="relative flex items-center gap-1.5  "><div class="mr-2 inline-flex h-6 items-center overflow-hidden whitespace-nowrap rounded-md border text-sm text-gray-500"><button class="focus:outline-hidden relative flex h-full max-w-56 items-center gap-1.5 overflow-hidden px-1.5 hover:bg-gray-50 focus:bg-gray-100 dark:hover:bg-gray-900 dark:focus:bg-gray-800" type="button" ><div class="flex h-full flex-1 items-center justify-center ">Follow</div>
		<img alt="" class="rounded-xs size-3 flex-none select-none" src="https://cdn-avatars.huggingface.co/v1/production/uploads/1664140778418-6330c479c375586dc3b2aa2c.jpeg" loading="lazy">
		<span class="truncate">HDR Imageomics Institute</span></button>
	<button class="focus:outline-hidden flex h-full items-center border-l pl-1.5 pr-1.5 text-gray-400 hover:bg-gray-50 focus:bg-gray-100 dark:hover:bg-gray-900 dark:focus:bg-gray-800" title="Show HDR Imageomics Institute's followers" type="button">148</button></div>

		</div>
			
	</h1>
		<div class="mb-3 flex flex-wrap md:mb-4">
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?pipeline_tag=zero-shot-image-classification"><div class="tag   tag-white "><div class="tag-ico -ml-2 tag-ico-blue"><svg class="-mr-0.5" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" fill="currentColor" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 18 19"><path d="M12.3625 13.85H10.1875V12.7625H12.3625V10.5875H13.45V12.7625C13.4497 13.0508 13.335 13.3272 13.1312 13.5311C12.9273 13.735 12.6508 13.8497 12.3625 13.85V13.85Z"></path><path d="M5.8375 8.41246H4.75V6.23746C4.75029 5.94913 4.86496 5.67269 5.06884 5.4688C5.27272 5.26492 5.54917 5.15025 5.8375 5.14996H8.0125V6.23746H5.8375V8.41246Z"></path><path d="M15.625 5.14998H13.45V2.97498C13.4497 2.68665 13.335 2.4102 13.1312 2.20632C12.9273 2.00244 12.6508 1.88777 12.3625 1.88748H2.575C2.28666 1.88777 2.01022 2.00244 1.80633 2.20632C1.60245 2.4102 1.48778 2.68665 1.4875 2.97498V12.7625C1.48778 13.0508 1.60245 13.3273 1.80633 13.5311C2.01022 13.735 2.28666 13.8497 2.575 13.85H4.75V16.025C4.75028 16.3133 4.86495 16.5898 5.06883 16.7936C5.27272 16.9975 5.54916 17.1122 5.8375 17.1125H15.625C15.9133 17.1122 16.1898 16.9975 16.3937 16.7936C16.5975 16.5898 16.7122 16.3133 16.7125 16.025V6.23748C16.7122 5.94915 16.5975 5.6727 16.3937 5.46882C16.1898 5.26494 15.9133 5.15027 15.625 5.14998V5.14998ZM15.625 16.025H5.8375V13.85H8.0125V12.7625H5.8375V10.5875H4.75V12.7625H2.575V2.97498H12.3625V5.14998H10.1875V6.23748H12.3625V8.41248H13.45V6.23748H15.625V16.025Z"></path></svg></div>

	

	<span>Zero-Shot Image Classification</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?library=open_clip"><div class="tag   tag-white ">

	

	<span>OpenCLIP</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?library=safetensors"><div class="tag   tag-white "><svg class="text-black inline-block text-sm" viewBox="0 0 57 44" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet"><path d="M36.816 20.1474L54.9918 27.4409C55.5142 27.6506 55.9623 28.0112 56.2788 28.4766C56.5954 28.9421 56.7661 29.4913 56.7691 30.0542C56.7722 30.6171 56.6074 31.1682 56.2959 31.637C55.9844 32.1059 55.5402 32.4713 55.0201 32.6866L29.953 43.0646C29.2593 43.3518 28.4799 43.3518 27.7862 43.0646L2.71624 32.6894C2.19613 32.4741 1.75197 32.1087 1.44044 31.6398C1.12892 31.171 0.964165 30.62 0.967204 30.057C0.970244 29.4941 1.14094 28.9449 1.45751 28.4794C1.77408 28.014 2.22216 27.6534 2.74456 27.4437L21.2404 20.0227C22.2997 19.5979 25.6477 20.8441 28.8682 20.8555C32.3096 20.8668 35.6292 19.6715 36.816 20.1474ZM11.3042 30.1119L28.8682 37.3828L46.435 30.1119L28.8682 23.0619L11.3042 30.1119ZM29.9247 0.388251L54.9918 10.4462C55.5142 10.6559 55.9623 11.0165 56.2788 11.482C56.5954 11.9474 56.7661 12.4967 56.7691 13.0596C56.7722 13.6225 56.6074 14.1735 56.2959 14.6424C55.9844 15.1112 55.5402 15.4766 55.0201 15.6919L29.953 26.07C29.2593 26.3572 28.4799 26.3572 27.7862 26.07L2.71624 15.6948C2.19613 15.4795 1.75197 15.1141 1.44044 14.6452C1.12892 14.1763 0.964165 13.6253 0.967204 13.0624C0.970244 12.4995 1.14094 11.9503 1.45751 11.4848C1.77408 11.0193 2.22216 10.6588 2.74456 10.4491L27.8117 0.388251C28.4896 0.1157 29.2467 0.1157 29.9247 0.388251ZM11.3042 13.1172L28.8682 20.3881L46.435 13.1172L28.8682 6.06729L11.3042 13.1172Z" fill="currentColor"></path></svg>

	

	<span>Safetensors</span>
	

	</div></a>
			
		<button class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" type="button"><div class="tag   tag-white ">
		<svg class="-mr-1 text-red-500" style="" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 25 25"><ellipse cx="12.5" cy="5" fill="currentColor" fill-opacity="0.25" rx="7.5" ry="2"></ellipse><path d="M12.5 15C16.6421 15 20 14.1046 20 13V20C20 21.1046 16.6421 22 12.5 22C8.35786 22 5 21.1046 5 20V13C5 14.1046 8.35786 15 12.5 15Z" fill="currentColor" opacity="0.5"></path><path d="M12.5 7C16.6421 7 20 6.10457 20 5V11.5C20 12.6046 16.6421 13.5 12.5 13.5C8.35786 13.5 5 12.6046 5 11.5V5C5 6.10457 8.35786 7 12.5 7Z" fill="currentColor" opacity="0.5"></path><path d="M5.23628 12C5.08204 12.1598 5 12.8273 5 13C5 14.1046 8.35786 15 12.5 15C16.6421 15 20 14.1046 20 13C20 12.8273 19.918 12.1598 19.7637 12C18.9311 12.8626 15.9947 13.5 12.5 13.5C9.0053 13.5 6.06886 12.8626 5.23628 12Z" fill="currentColor"></path></svg>

	

	<span>5 datasets</span>
	

	</div></button>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?language=en"><div class="tag   tag-white ">
		<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="text-green-600/80" preserveAspectRatio="xMidYMid meet" width="1em" height="1em" viewBox="0 0 10 10"><path fill-rule="evenodd" clip-rule="evenodd" d="M0.625 5C0.625 6.16032 1.08594 7.27312 1.90641 8.09359C2.72688 8.91406 3.83968 9.375 5 9.375C6.16032 9.375 7.27312 8.91406 8.09359 8.09359C8.91406 7.27312 9.375 6.16032 9.375 5C9.375 3.83968 8.91406 2.72688 8.09359 1.90641C7.27312 1.08594 6.16032 0.625 5 0.625C3.83968 0.625 2.72688 1.08594 1.90641 1.90641C1.08594 2.72688 0.625 3.83968 0.625 5ZM7.64365 7.48027C7.61734 7.50832 7.59054 7.53598 7.56326 7.56326C7.13828 7.98824 6.61864 8.2968 6.0539 8.46842C6.29802 8.11949 6.49498 7.64804 6.63475 7.09483C7.00845 7.18834 7.35014 7.3187 7.64365 7.48027ZM8.10076 6.87776C8.37677 6.42196 8.55005 5.90894 8.60556 5.37499H6.86808C6.85542 5.71597 6.82551 6.04557 6.77971 6.35841C7.25309 6.47355 7.68808 6.6414 8.062 6.85549C8.07497 6.86283 8.08789 6.87025 8.10076 6.87776ZM6.03795 6.22536C6.07708 5.95737 6.1044 5.67232 6.11705 5.37499H3.88295C3.89666 5.69742 3.92764 6.00542 3.9722 6.29287C4.37075 6.21726 4.79213 6.17749 5.224 6.17749C5.50054 6.17749 5.77294 6.19376 6.03795 6.22536ZM4.1261 7.02673C4.34894 7.84835 4.68681 8.375 5 8.375C5.32122 8.375 5.66839 7.82101 5.8908 6.963C5.67389 6.93928 5.45082 6.92699 5.224 6.92699C4.84316 6.92699 4.47332 6.96176 4.1261 7.02673ZM3.39783 7.21853C3.53498 7.71842 3.72038 8.14579 3.9461 8.46842C3.42141 8.30898 2.93566 8.03132 2.52857 7.65192C2.77253 7.48017 3.06711 7.33382 3.39783 7.21853ZM3.23916 6.48077C3.18263 6.13193 3.14625 5.76074 3.13192 5.37499H1.39444C1.4585 5.99112 1.67936 6.57938 2.03393 7.08403C2.3706 6.83531 2.78055 6.63162 3.23916 6.48077ZM1.39444 4.62499H3.13192C3.14615 4.24204 3.18211 3.87344 3.23794 3.52681C2.77814 3.37545 2.36731 3.17096 2.03024 2.92123C1.67783 3.42469 1.45828 4.011 1.39444 4.62499ZM2.5237 2.35262C2.76812 2.52552 3.06373 2.67281 3.39584 2.78875C3.53318 2.28573 3.71928 1.85578 3.9461 1.53158C3.41932 1.69166 2.93178 1.97089 2.5237 2.35262ZM3.97101 3.71489C3.92709 4.00012 3.89654 4.30547 3.88295 4.62499H6.11705C6.10453 4.33057 6.07761 4.04818 6.03909 3.78248C5.77372 3.81417 5.50093 3.83049 5.224 3.83049C4.79169 3.83049 4.3699 3.79065 3.97101 3.71489ZM5.8928 3.04476C5.67527 3.06863 5.45151 3.08099 5.224 3.08099C4.84241 3.08099 4.47186 3.04609 4.12405 2.98086C4.34686 2.1549 4.68584 1.625 5 1.625C5.32218 1.625 5.67048 2.18233 5.8928 3.04476ZM6.78083 3.6493C6.826 3.95984 6.85552 4.28682 6.86808 4.62499H8.60556C8.55029 4.09337 8.37827 3.58251 8.10436 3.1282C8.0903 3.1364 8.07618 3.14449 8.062 3.15249C7.68838 3.36641 7.25378 3.53417 6.78083 3.6493ZM7.64858 2.52499C7.35446 2.68754 7.0117 2.81868 6.63664 2.91268C6.49676 2.35623 6.29913 1.88209 6.0539 1.53158C6.61864 1.7032 7.13828 2.01176 7.56326 2.43674C7.59224 2.46572 7.62068 2.49514 7.64858 2.52499Z" fill="currentColor"></path></svg>

	

	<span>English</span>
	

	</div></a>

	<div class="relative inline-block ">
	<button class="group mr-1 mb-1 md:mr-1.5 md:mb-1.5  rounded-lg rounded-br-none " type="button">
		<div slot="button"><div class="tag   tag-white relative rounded-br-none pr-2.5">

	

	<span>doi:10.57967/hf/6799</span>
	

	<div class="border-br-gray-200 absolute bottom-0.5 right-0.5 h-1 w-1 border-[3px] border-l-transparent border-t-transparent border-b-gray-200 border-r-gray-200 group-hover:border-b-gray-400 group-hover:border-r-gray-400 dark:border-b-gray-700 dark:border-r-gray-700 group-hover:dark:border-b-gray-400 group-hover:dark:border-r-gray-400"></div></div></div>
		</button>
	
	
	</div>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=biology"><div class="tag   tag-white ">

	

	<span>biology</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=CV"><div class="tag   tag-white ">

	

	<span>CV</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=images"><div class="tag   tag-white ">

	

	<span>images</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=imageomics"><div class="tag   tag-white ">

	

	<span>imageomics</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=clip"><div class="tag   tag-white ">

	

	<span>clip</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=species-classification"><div class="tag   tag-white ">

	

	<span>species-classification</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=biological+visual+task"><div class="tag   tag-white ">

	

	<span>biological visual task</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=multimodal"><div class="tag   tag-white ">

	

	<span>multimodal</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=animals"><div class="tag   tag-white ">

	

	<span>animals</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=plants"><div class="tag   tag-white ">

	

	<span>plants</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=fungi"><div class="tag   tag-white ">

	

	<span>fungi</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=species"><div class="tag   tag-white ">

	

	<span>species</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=taxonomy"><div class="tag   tag-white ">

	

	<span>taxonomy</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=rare+species"><div class="tag   tag-white ">

	

	<span>rare species</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=endangered+species"><div class="tag   tag-white ">

	

	<span>endangered species</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=evolutionary+biology"><div class="tag   tag-white ">

	

	<span>evolutionary biology</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=knowledge-guided"><div class="tag   tag-white ">

	

	<span>knowledge-guided</span>
	

	</div></a>
		<a class="mb-1 mr-1 md:mb-1.5 md:mr-1.5 rounded-lg" href="/models?other=zero-shot-text-retrieval"><div class="tag   tag-white ">

	

	<span>zero-shot-text-retrieval</span>
	

	</div></a>

	<div class="relative inline-block ">
	<button class="group mr-1 mb-1 md:mr-1.5 md:mb-1.5  rounded-full rounded-br-none " type="button">
		<div slot="button"><div class="tag rounded-full  tag-white relative rounded-br-none pr-2.5">
		<svg class="-mr-1 text-gray-400" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" viewBox="0 0 12 12" preserveAspectRatio="xMidYMid meet" fill="none"><path fill="currentColor" fill-rule="evenodd" d="M8.007 1.814a1.176 1.176 0 0 0-.732-.266H3.088c-.64 0-1.153.512-1.153 1.152v6.803c0 .64.513 1.152 1.153 1.152h5.54c.632 0 1.144-.511 1.144-1.152V3.816c0-.338-.137-.658-.412-.887L8.007 1.814Zm-1.875 1.81c0 .695.55 1.253 1.244 1.253h.983a.567.567 0 0 1 .553.585v4.041c0 .165-.119.302-.283.302h-5.55c-.156 0-.275-.137-.275-.302V2.7a.284.284 0 0 1 .284-.301h2.468a.574.574 0 0 1 .434.19.567.567 0 0 1 .142.395v.64Z" clip-rule="evenodd" fill-opacity=".8"></path><path fill="currentColor" fill-opacity=".2" fill-rule="evenodd" d="M6.132 3.624c0 .695.55 1.253 1.244 1.253h.97a.567.567 0 0 1 .566.585v4.041c0 .165-.119.302-.283.302h-5.55c-.156 0-.275-.137-.275-.302V2.7a.284.284 0 0 1 .284-.301h2.468a.567.567 0 0 1 .576.585v.64Z" clip-rule="evenodd"></path></svg>

	

	<span class="-mr-2 text-gray-400">arxiv:</span>
		<span>2510.20095</span>
	

	<div class="border-br-gray-200 absolute bottom-0.5 right-0.5 h-1 w-1 border-[3px] border-l-transparent border-t-transparent border-b-gray-200 border-r-gray-200 group-hover:border-b-gray-400 group-hover:border-r-gray-400 dark:border-b-gray-700 dark:border-r-gray-700 group-hover:dark:border-b-gray-400 group-hover:dark:border-r-gray-400"></div></div></div>
		</button>
	
	
	</div><div class="relative inline-block ">
	<button class="group mr-1 mb-1 md:mr-1.5 md:mb-1.5  rounded-full rounded-br-none " type="button">
		<div slot="button"><div class="tag rounded-full  tag-white relative rounded-br-none pr-2.5">
		<svg class="text-xs text-gray-900" width="1em" height="1em" viewBox="0 0 10 10" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1.46009 5.0945V6.88125C1.46009 7.25201 1.75937 7.55129 2.13012 7.55129C2.50087 7.55129 2.80016 7.25201 2.80016 6.88125V5.0945C2.80016 4.72375 2.50087 4.42446 2.13012 4.42446C1.75937 4.42446 1.46009 4.72375 1.46009 5.0945ZM4.14022 5.0945V6.88125C4.14022 7.25201 4.4395 7.55129 4.81026 7.55129C5.18101 7.55129 5.48029 7.25201 5.48029 6.88125V5.0945C5.48029 4.72375 5.18101 4.42446 4.81026 4.42446C4.4395 4.42446 4.14022 4.72375 4.14022 5.0945ZM1.23674 9.78473H8.38377C8.75452 9.78473 9.0538 9.48545 9.0538 9.1147C9.0538 8.74395 8.75452 8.44466 8.38377 8.44466H1.23674C0.865993 8.44466 0.566711 8.74395 0.566711 9.1147C0.566711 9.48545 0.865993 9.78473 1.23674 9.78473ZM6.82036 5.0945V6.88125C6.82036 7.25201 7.11964 7.55129 7.49039 7.55129C7.86114 7.55129 8.16042 7.25201 8.16042 6.88125V5.0945C8.16042 4.72375 7.86114 4.42446 7.49039 4.42446C7.11964 4.42446 6.82036 4.72375 6.82036 5.0945ZM4.39484 0.623142L0.865993 2.48137C0.682851 2.57517 0.566711 2.76725 0.566711 2.97273C0.566711 3.28094 0.816857 3.53109 1.12507 3.53109H8.49991C8.80365 3.53109 9.0538 3.28094 9.0538 2.97273C9.0538 2.76725 8.93766 2.57517 8.75452 2.48137L5.22568 0.623142C4.9666 0.484669 4.65391 0.484669 4.39484 0.623142V0.623142Z" fill="currentColor"></path></svg>

	<span class="-mr-1 text-gray-400">License:</span>

	<span>mit</span>
	

	<div class="border-br-gray-200 absolute bottom-0.5 right-0.5 h-1 w-1 border-[3px] border-l-transparent border-t-transparent border-b-gray-200 border-r-gray-200 group-hover:border-b-gray-400 group-hover:border-r-gray-400 dark:border-b-gray-700 dark:border-r-gray-700 group-hover:dark:border-b-gray-400 group-hover:dark:border-r-gray-400"></div></div></div>
		</button>
	
	
	</div></div>

		<div class="flex flex-col-reverse lg:flex-row lg:items-center lg:justify-between"><div class="-mb-px flex h-12 items-center overflow-x-auto overflow-y-hidden ">
	<a class="tab-alternate" href="/imageomics/biocap"><svg class="mr-1.5 text-gray-400 flex-none" style="" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path class="uim-quaternary" d="M20.23 7.24L12 12L3.77 7.24a1.98 1.98 0 0 1 .7-.71L11 2.76c.62-.35 1.38-.35 2 0l6.53 3.77c.29.173.531.418.7.71z" opacity=".25" fill="currentColor"></path><path class="uim-tertiary" d="M12 12v9.5a2.09 2.09 0 0 1-.91-.21L4.5 17.48a2.003 2.003 0 0 1-1-1.73v-7.5a2.06 2.06 0 0 1 .27-1.01L12 12z" opacity=".5" fill="currentColor"></path><path class="uim-primary" d="M20.5 8.25v7.5a2.003 2.003 0 0 1-1 1.73l-6.62 3.82c-.275.13-.576.198-.88.2V12l8.23-4.76c.175.308.268.656.27 1.01z" fill="currentColor"></path></svg>
	Model card
	

	
		</a><a class="tab-alternate active" href="/imageomics/biocap/tree/main"><svg class="mr-1.5 text-gray-400 flex-none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path class="uim-tertiary" d="M21 19h-8a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2zm0-4h-8a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2zm0-8h-8a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2zm0 4h-8a1 1 0 0 1 0-2h8a1 1 0 0 1 0 2z" opacity=".5" fill="currentColor"></path><path class="uim-primary" d="M9 19a1 1 0 0 1-1-1V6a1 1 0 0 1 2 0v12a1 1 0 0 1-1 1zm-6-4.333a1 1 0 0 1-.64-1.769L3.438 12l-1.078-.898a1 1 0 0 1 1.28-1.538l2 1.667a1 1 0 0 1 0 1.538l-2 1.667a.999.999 0 0 1-.64.231z" fill="currentColor"></path></svg>
	<span class="xl:hidden">Files</span>
		<span class="hidden xl:inline">Files and versions</span>
	

	

<span class="inline-block "><span class="contents"><div slot="anchor" class="shadow-purple-500/10 ml-2 inline-flex -translate-y-px items-center gap-0.5 rounded-md border bg-white px-1 py-0.5 align-middle text-xs font-semibold leading-none text-gray-800 shadow-sm dark:border-gray-700 dark:bg-gradient-to-b dark:from-gray-925 dark:to-gray-925 dark:text-gray-300"><svg class="size-3 " xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="currentColor" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 12 12"><path fill-rule="evenodd" clip-rule="evenodd" d="M6.14 3.64 5.1 4.92 2.98 2.28h2.06l1.1 1.36Zm0 4.72-1.1 1.36H2.98l2.13-2.64 1.03 1.28Zm4.9 1.36L8.03 6l3-3.72H8.96L5.97 6l3 3.72h2.06Z" fill="#7875FF"></path><path d="M4.24 6 2.6 8.03.97 6 2.6 3.97 4.24 6Z" fill="#FF7F41" opacity="1"></path></svg>
						<span>xet</span>
					</div></span>
	</span>
		</a><a class="tab-alternate" href="/imageomics/biocap/discussions"><svg class="mr-1.5 text-gray-400 flex-none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M20.6081 3C21.7684 3 22.8053 3.49196 23.5284 4.38415C23.9756 4.93678 24.4428 5.82749 24.4808 7.16133C24.9674 7.01707 25.4353 6.93643 25.8725 6.93643C26.9833 6.93643 27.9865 7.37587 28.696 8.17411C29.6075 9.19872 30.0124 10.4579 29.8361 11.7177C29.7523 12.3177 29.5581 12.8555 29.2678 13.3534C29.8798 13.8646 30.3306 14.5763 30.5485 15.4322C30.719 16.1032 30.8939 17.5006 29.9808 18.9403C30.0389 19.0342 30.0934 19.1319 30.1442 19.2318C30.6932 20.3074 30.7283 21.5229 30.2439 22.6548C29.5093 24.3704 27.6841 25.7219 24.1397 27.1727C21.9347 28.0753 19.9174 28.6523 19.8994 28.6575C16.9842 29.4379 14.3477 29.8345 12.0653 29.8345C7.87017 29.8345 4.8668 28.508 3.13831 25.8921C0.356375 21.6797 0.754104 17.8269 4.35369 14.1131C6.34591 12.058 7.67023 9.02782 7.94613 8.36275C8.50224 6.39343 9.97271 4.20438 12.4172 4.20438H12.4179C12.6236 4.20438 12.8314 4.2214 13.0364 4.25468C14.107 4.42854 15.0428 5.06476 15.7115 6.02205C16.4331 5.09583 17.134 4.359 17.7682 3.94323C18.7242 3.31737 19.6794 3 20.6081 3ZM20.6081 5.95917C20.2427 5.95917 19.7963 6.1197 19.3039 6.44225C17.7754 7.44319 14.8258 12.6772 13.7458 14.7131C13.3839 15.3952 12.7655 15.6837 12.2086 15.6837C11.1036 15.6837 10.2408 14.5497 12.1076 13.1085C14.9146 10.9402 13.9299 7.39584 12.5898 7.1776C12.5311 7.16799 12.4731 7.16355 12.4172 7.16355C11.1989 7.16355 10.6615 9.33114 10.6615 9.33114C10.6615 9.33114 9.0863 13.4148 6.38031 16.206C3.67434 18.998 3.5346 21.2388 5.50675 24.2246C6.85185 26.2606 9.42666 26.8753 12.0653 26.8753C14.8021 26.8753 17.6077 26.2139 19.1799 25.793C19.2574 25.7723 28.8193 22.984 27.6081 20.6107C27.4046 20.212 27.0693 20.0522 26.6471 20.0522C24.9416 20.0522 21.8393 22.6726 20.5057 22.6726C20.2076 22.6726 19.9976 22.5416 19.9116 22.222C19.3433 20.1173 28.552 19.2325 27.7758 16.1839C27.639 15.6445 27.2677 15.4256 26.746 15.4263C24.4923 15.4263 19.4358 19.5181 18.3759 19.5181C18.2949 19.5181 18.2368 19.4937 18.2053 19.4419C17.6743 18.557 17.9653 17.9394 21.7082 15.6009C25.4511 13.2617 28.0783 11.8545 26.5841 10.1752C26.4121 9.98141 26.1684 9.8956 25.8725 9.8956C23.6001 9.89634 18.2311 14.9403 18.2311 14.9403C18.2311 14.9403 16.7821 16.496 15.9057 16.496C15.7043 16.496 15.533 16.4139 15.4169 16.2112C14.7956 15.1296 21.1879 10.1286 21.5484 8.06535C21.7928 6.66715 21.3771 5.95917 20.6081 5.95917Z" fill="#FF9D00"></path><path d="M5.50686 24.2246C3.53472 21.2387 3.67446 18.9979 6.38043 16.206C9.08641 13.4147 10.6615 9.33111 10.6615 9.33111C10.6615 9.33111 11.2499 6.95933 12.59 7.17757C13.93 7.39581 14.9139 10.9401 12.1069 13.1084C9.29997 15.276 12.6659 16.7489 13.7459 14.713C14.8258 12.6772 17.7747 7.44316 19.304 6.44221C20.8326 5.44128 21.9089 6.00204 21.5484 8.06532C21.188 10.1286 14.795 15.1295 15.4171 16.2118C16.0391 17.2934 18.2312 14.9402 18.2312 14.9402C18.2312 14.9402 25.0907 8.49588 26.5842 10.1752C28.0776 11.8545 25.4512 13.2616 21.7082 15.6008C17.9646 17.9393 17.6744 18.557 18.2054 19.4418C18.7372 20.3266 26.9998 13.1351 27.7759 16.1838C28.5513 19.2324 19.3434 20.1173 19.9117 22.2219C20.48 24.3274 26.3979 18.2382 27.6082 20.6107C28.8193 22.9839 19.2574 25.7722 19.18 25.7929C16.0914 26.62 8.24723 28.3726 5.50686 24.2246Z" fill="#FFD21E"></path></svg>
	Community
	

	
		</a></div>
	
			


<div class="relative mb-1.5 flex flex-wrap gap-1.5 sm:flex-nowrap lg:mb-0"><div class="order-last sm:order-first"><div class="relative ">
	<button class="btn px-1.5 py-1.5 " type="button">
		
			<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="p-0.5" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><circle cx="16" cy="7" r="3" fill="currentColor"></circle><circle cx="16" cy="16" r="3" fill="currentColor"></circle><circle cx="16" cy="25" r="3" fill="currentColor"></circle></svg>
		
		</button>
	
	
	</div></div>

<dialog class="shadow-alternate z-40 mx-4 my-auto h-fit select-text overflow-hidden rounded-xl bg-white max-sm:max-w-[calc(100dvw-2rem)] sm:mx-auto lg:mt-26 md:portrait:mt-30 xl:mt-30 2xl:mt-32 w-full lg:w-10/12 xl:w-8/12 2xl:w-7/12 max-w-[calc(100%-4rem)] lg:max-w-4xl ">
	<div tabindex="-1" class="outline-none focus:ring-0 focus-visible:ring-0"></div></dialog>

<dialog class="shadow-alternate z-40 mx-4 my-auto h-fit select-text overflow-hidden rounded-xl bg-white max-sm:max-w-[calc(100dvw-2rem)] sm:mx-auto lg:mt-26 md:portrait:mt-30 xl:mt-30 2xl:mt-32 w-full lg:w-7/12 max-w-[calc(100%-4rem)] md:max-w-2xl ">
	<div tabindex="-1" class="outline-none focus:ring-0 focus-visible:ring-0"></div></dialog>










	
		<div class="relative flex-auto sm:flex-none">
	<button class="from-gray-800! to-black! text-white! gap-1! border-gray-800! dark:border-gray-900!  btn w-full cursor-pointer text-sm" type="button">
		<svg class="mr-1.5 mr-0.5! " xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path fill="currentColor" d="M28 4H4a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h8v4H8v2h16v-2h-4v-4h8a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2ZM18 28h-4v-4h4Zm10-6H4V6h24Z"></path></svg>
			Use this model
		<svg class="-mr-1 text-gray-500 " xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path d="M16.293 9.293L12 13.586L7.707 9.293l-1.414 1.414L12 16.414l5.707-5.707z" fill="currentColor"></path></svg></button>
	
	
	</div>



</div>
	</div></div></header>
<dialog class="shadow-alternate z-40 mx-4 my-auto h-fit select-text overflow-hidden rounded-xl bg-white max-sm:max-w-[calc(100dvw-2rem)] sm:mx-auto lg:mt-26 md:portrait:mt-30 xl:mt-30 2xl:mt-32 w-full sm:w-96 max-w-[calc(100%-4rem)] text-base ">
	<div tabindex="-1" class="outline-none focus:ring-0 focus-visible:ring-0"></div></dialog></div>
	
<div class="container relative flex flex-col md:grid md:space-y-0 w-full md:grid-cols-12  space-y-4 md:gap-6 mb-16"><section class="pt-8 border-gray-100 col-span-full"><div class="SVELTE_HYDRATER contents" data-target="ViewerHeader" data-props="{&quot;context&quot;:{&quot;repo&quot;:{&quot;name&quot;:&quot;imageomics/biocap&quot;,&quot;type&quot;:&quot;model&quot;},&quot;rev&quot;:&quot;main&quot;,&quot;path&quot;:&quot;README.md&quot;,&quot;subpaths&quot;:[{&quot;dir&quot;:&quot;README.md&quot;}]},&quot;refs&quot;:{&quot;branches&quot;:[{&quot;name&quot;:&quot;main&quot;,&quot;ref&quot;:&quot;refs/heads/main&quot;,&quot;targetCommit&quot;:&quot;4e544d1d08781b6afee77bd7c1a85d04bd567d1b&quot;}],&quot;tags&quot;:[],&quot;converts&quot;:[]},&quot;view&quot;:&quot;blob&quot;,&quot;isMac&quot;:false}"><header class="flex flex-wrap items-center justify-start pb-2 md:justify-end lg:flex-nowrap"><div class="grow max-md:flex max-md:w-full max-md:items-start max-md:justify-between"><div class="relative mr-4 flex min-w-0 basis-auto flex-wrap items-center gap-x-3 md:grow md:basis-full lg:basis-auto lg:flex-nowrap"><div class="relative mb-2">
	<button class="text-sm md:text-base btn w-full cursor-pointer text-sm" type="button">
		<svg class="mr-1.5 text-gray-700 dark:text-gray-400" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24" style="transform: rotate(360deg);"><path d="M13 14c-3.36 0-4.46 1.35-4.82 2.24C9.25 16.7 10 17.76 10 19a3 3 0 0 1-3 3a3 3 0 0 1-3-3c0-1.31.83-2.42 2-2.83V7.83A2.99 2.99 0 0 1 4 5a3 3 0 0 1 3-3a3 3 0 0 1 3 3c0 1.31-.83 2.42-2 2.83v5.29c.88-.65 2.16-1.12 4-1.12c2.67 0 3.56-1.34 3.85-2.23A3.006 3.006 0 0 1 14 7a3 3 0 0 1 3-3a3 3 0 0 1 3 3c0 1.34-.88 2.5-2.09 2.86C17.65 11.29 16.68 14 13 14m-6 4a1 1 0 0 0-1 1a1 1 0 0 0 1 1a1 1 0 0 0 1-1a1 1 0 0 0-1-1M7 4a1 1 0 0 0-1 1a1 1 0 0 0 1 1a1 1 0 0 0 1-1a1 1 0 0 0-1-1m10 2a1 1 0 0 0-1 1a1 1 0 0 0 1 1a1 1 0 0 0 1-1a1 1 0 0 0-1-1z" fill="currentColor"></path></svg>
			main
		<svg class="-mr-1 text-gray-500 " xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path d="M16.293 9.293L12 13.586L7.707 9.293l-1.414 1.414L12 16.414l5.707-5.707z" fill="currentColor"></path></svg></button>
	
	
	</div>
			<div class="relative mb-2 flex flex-wrap items-center"><a class="truncate text-gray-800 hover:underline" href="/imageomics/biocap/tree/main">biocap</a>
				<span class="mx-1 text-gray-300">/</span>
					<span class="dark:text-gray-300">README.md</span>
					<button class="text-xs ml-2 focus:outline-hidden inline-flex cursor-pointer items-center text-sm  mx-0.5   text-gray-600 " title="Copy path" type="button"><svg class="" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="currentColor" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M28,10V28H10V10H28m0-2H10a2,2,0,0,0-2,2V28a2,2,0,0,0,2,2H28a2,2,0,0,0,2-2V10a2,2,0,0,0-2-2Z" transform="translate(0)"></path><path d="M4,18H2V4A2,2,0,0,1,4,2H18V4H4Z" transform="translate(0)"></path><rect fill="none" width="32" height="32"></rect></svg>
		</button></div>
			</div>
		</div>
	
	</header></div>
			<div class="SVELTE_HYDRATER contents" data-target="LastCommit" data-props="{&quot;commitLast&quot;:{&quot;date&quot;:&quot;2025-10-24T13:56:09.000Z&quot;,&quot;verified&quot;:&quot;verified&quot;,&quot;subject&quot;:&quot;fix DOI citation&quot;,&quot;authors&quot;:[{&quot;_id&quot;:&quot;642dbba7c3a53b9e1d6e8726&quot;,&quot;avatar&quot;:&quot;https://cdn-avatars.huggingface.co/v1/production/uploads/642dbba7c3a53b9e1d6e8726/9ifixpoG2cu91WPAdsg-_.jpeg&quot;,&quot;isHf&quot;:false,&quot;user&quot;:&quot;egrace479&quot;}],&quot;commit&quot;:{&quot;id&quot;:&quot;4e544d1d08781b6afee77bd7c1a85d04bd567d1b&quot;,&quot;parentIds&quot;:[&quot;af8db7ab8965a2769c8613cfe8bfaf2f4d9de1b5&quot;]},&quot;title&quot;:&quot;fix DOI citation&quot;},&quot;repo&quot;:{&quot;name&quot;:&quot;imageomics/biocap&quot;,&quot;type&quot;:&quot;model&quot;}}"><div class="from-gray-100-to-white bg-linear-to-t flex flex-wrap items-baseline gap-y-1 rounded-t-lg border border-b-0 px-3 py-2 dark:border-gray-800"><img class="mr-2.5 mt-0.5 h-4 w-4 self-center rounded-full" alt="egrace479's picture" src="https://cdn-avatars.huggingface.co/v1/production/uploads/642dbba7c3a53b9e1d6e8726/9ifixpoG2cu91WPAdsg-_.jpeg">
			<div class="mr-4 flex flex-none items-center truncate"><a class="hover:underline" href="/egrace479">egrace479
					</a>
				
			</div>
		<div class="mr-4 truncate font-mono text-xs text-gray-500 hover:prose-a:underline sm:text-sm"><!-- HTML_TAG_START -->fix DOI citation<!-- HTML_TAG_END --></div>
		<a class="rounded-sm border bg-gray-50 px-1.5 text-sm hover:underline dark:border-gray-800 dark:bg-gray-900" href="/imageomics/biocap/commit/4e544d1d08781b6afee77bd7c1a85d04bd567d1b">4e544d1</a>
		<span class="mx-2 text-green-500 dark:text-green-600 px-1.5 border-green-100 dark:border-green-800 rounded-full border text-xs uppercase" title="This commit is signed and the signature is verified">verified</span>
		<time class="ml-auto hidden flex-none truncate pl-2 text-gray-500 dark:text-gray-400 lg:block" datetime="2025-10-24T13:56:09" title="Fri, 24 Oct 2025 13:56:09 GMT">3 months ago</time></div></div>
			<div class="relative flex flex-wrap items-center border px-3 py-1.5 text-sm text-gray-800 dark:border-gray-800 dark:bg-gray-900 "><div class="flex items-center gap-3 text-sm font-medium"><a class="rounded-md px-1.5 capitalize bg-gray-200 dark:bg-gray-800" href="/imageomics/biocap/blob/main/README.md">preview</a>
						<a class="rounded-md px-1.5 capitalize " href="/imageomics/biocap/blob/main/README.md?code=true">code</a></div>
					<div class="mx-4 text-gray-200">|</div>
				<a class="group my-1 mr-4 flex items-center " href="/imageomics/biocap/raw/main/README.md"><span class="flex items-center group-hover:underline"><svg class="mr-1.5" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32" style="transform: rotate(360deg);"><path d="M31 16l-7 7l-1.41-1.41L28.17 16l-5.58-5.59L24 9l7 7z" fill="currentColor"></path><path d="M1 16l7-7l1.41 1.41L3.83 16l5.58 5.59L8 23l-7-7z" fill="currentColor"></path><path d="M12.419 25.484L17.639 6l1.932.518L14.35 26z" fill="currentColor"></path></svg>
								raw</span>
							
						</a><div class="SVELTE_HYDRATER contents" data-target="CopyButton" data-props="{&quot;value&quot;:&quot;https://huggingface.co/imageomics/biocap/resolve/main/README.md&quot;,&quot;style&quot;:&quot;blank&quot;,&quot;label&quot;:&quot;Copy download link&quot;,&quot;classNames&quot;:&quot;my-1 mr-4 flex items-center no-underline hover:underline&quot;}"><button class="my-1 mr-4 flex items-center no-underline hover:underline       " title="Copy download link" type="button"><svg class="" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" fill="currentColor" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M28,10V28H10V10H28m0-2H10a2,2,0,0,0-2,2V28a2,2,0,0,0,2,2H28a2,2,0,0,0,2-2V10a2,2,0,0,0-2-2Z" transform="translate(0)"></path><path d="M4,18H2V4A2,2,0,0,1,4,2H18V4H4Z" transform="translate(0)"></path><rect fill="none" width="32" height="32"></rect></svg>
		<span class="ml-1.5 ">Copy download link</span></button></div><a class="group my-1 mr-4 flex items-center " href="/imageomics/biocap/commits/main/README.md"><span class="flex items-center group-hover:underline"><svg class="mr-1.5" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32" style="transform: rotate(360deg);"><path d="M16 4C9.383 4 4 9.383 4 16s5.383 12 12 12s12-5.383 12-12S22.617 4 16 4zm0 2c5.535 0 10 4.465 10 10s-4.465 10-10 10S6 21.535 6 16S10.465 6 16 6zm-1 2v9h7v-2h-5V8z" fill="currentColor"></path></svg>
								history</span>
							
						</a><a class="group my-1 mr-4 flex items-center " href="/imageomics/biocap/blame/main/README.md"><span class="flex items-center group-hover:underline"><svg class="mr-1.5" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32" style="transform: rotate(360deg);"><path d="M16 2a14 14 0 1 0 14 14A14 14 0 0 0 16 2zm0 26a12 12 0 1 1 12-12a12 12 0 0 1-12 12z" fill="currentColor"></path><path d="M11.5 11a2.5 2.5 0 1 0 2.5 2.5a2.48 2.48 0 0 0-2.5-2.5z" fill="currentColor"></path><path d="M20.5 11a2.5 2.5 0 1 0 2.5 2.5a2.48 2.48 0 0 0-2.5-2.5z" fill="currentColor"></path></svg>
								blame</span>
							
						</a><a class="group my-1 mr-4 flex items-center text-green-600 dark:text-green-500" href="/imageomics/biocap/edit/main/README.md"><span class="flex items-center group-hover:underline"><svg class="mr-1.5" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M2 26h28v2H2z" fill="currentColor"></path><path d="M25.4 9c.8-.8.8-2 0-2.8l-3.6-3.6c-.8-.8-2-.8-2.8 0l-15 15V24h6.4l15-15zm-5-5L24 7.6l-3 3L17.4 7l3-3zM6 22v-3.6l10-10l3.6 3.6l-10 10H6z" fill="currentColor"></path></svg>
								contribute</span>
							
						</a><a class="group my-1 mr-4 flex items-center " href="/imageomics/biocap/delete/main/README.md"><span class="flex items-center group-hover:underline"><svg class="mr-1.5" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M12 12h2v12h-2z" fill="currentColor"></path><path d="M18 12h2v12h-2z" fill="currentColor"></path><path d="M4 6v2h2v20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8h2V6zm4 22V8h16v20z" fill="currentColor"></path><path d="M12 2h8v2h-8z" fill="currentColor"></path></svg>
								delete</span>
							
						</a>

				

				<div class="flex items-center gap-x-3 dark:text-gray-300 sm:ml-auto">
					17.8 kB</div></div>

			<div class="relative min-h-[100px] rounded-b-lg border border-t-0 leading-tight dark:border-gray-800 dark:bg-gray-925">
				
				
						<div class="py-4 px-4 sm:px-6 prose hf-sanitized hf-sanitized-nZmdCmWixsboPLbFyApb2 copiable-code-container"><div class="not-prose bg-linear-to-t -mx-6 -mt-4 mb-8 max-h-[300px] min-w-full overflow-auto border-b from-gray-50 px-6 pb-5 pt-4 font-mono text-xs transition-all dark:from-gray-900 dark:to-gray-950"><a href="/docs/hub/model-cards#model-card-metadata" target="_blank" rel="noopener noreferrer" class="mb-2 inline-flex items-center gap-1 rounded-lg border px-2 py-1 font-mono text-xs leading-none hover:bg-gray-100 dark:hover:bg-gray-800">metadata <svg class="text-[0.6rem] opacity-70 translate-y-px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" focusable="false" role="img" width="1em" height="1em" preserveAspectRatio="xMidYMid meet" viewBox="0 0 32 32"><path d="M17 22v-8h-4v2h2v6h-3v2h8v-2h-3z" fill="currentColor"></path><path d="M16 8a1.5 1.5 0 1 0 1.5 1.5A1.5 1.5 0 0 0 16 8z" fill="currentColor"></path><path d="M16 30a14 14 0 1 1 14-14a14 14 0 0 1-14 14zm0-26a12 12 0 1 0 12 12A12 12 0 0 0 16 4z" fill="currentColor"></path></svg></a>
			<pre><!-- HTML_TAG_START --><span class="hljs-attr">license:</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">mit</span>
<span class="hljs-attr">language:</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">en</span>
<span class="hljs-attr">library_name:</span> <span class="hljs-string">open_clip</span>
<span class="hljs-attr">model_name:</span> <span class="hljs-string">BioCAP</span>
<span class="hljs-attr">model_description:</span> <span class="hljs-string">&gt;-</span>
<span class="hljs-string">  Foundation model for biology organismal images. It is trained on</span>
<span class="hljs-string">  TreeOfLife-10M with synthetic captions (TreeOfLife-10M-Captions) as</span>
<span class="hljs-string">  supervision on the basis of a CLIP model (ViT-B/16) pre-trained by openai.</span>
<span class="hljs-string">  BioCAP achieves state-of-the-art performance on text-image retrieval tasks.</span>
<span class="hljs-string"></span><span class="hljs-attr">tags:</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">biology</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">CV</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">images</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">imageomics</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">clip</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">species-classification</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">biological</span> <span class="hljs-string">visual</span> <span class="hljs-string">task</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">multimodal</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">animals</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">plants</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">fungi</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">species</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">taxonomy</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">rare</span> <span class="hljs-string">species</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">endangered</span> <span class="hljs-string">species</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">evolutionary</span> <span class="hljs-string">biology</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">knowledge-guided</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">zero-shot-image-classification</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">zero-shot-text-retrieval</span>
<span class="hljs-attr">datasets:</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">imageomics/TreeOfLife-10M-Captions</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">imageomics/TreeOfLife-10M</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">iNat21</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">BIOSCAN-1M</span>
  <span class="hljs-bullet">-</span> <span class="hljs-string">EOL</span>
<!-- HTML_TAG_END --></pre></div>
	<!-- HTML_TAG_START --><h1 class="relative group flex items-center">
	<a rel="nofollow" href="#model-card-for-biocap" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="model-card-for-biocap">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Model Card for BioCAP
	</span>
</h1>
<p>BioCAP is a foundation model for biology organismal images. It is trained on <a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M">TreeOfLife-10M</a> with synthetic captions (<a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M-Captions">TreeOfLife-10M-Captions</a>) as supervision on the basis of a <a rel="nofollow" href="https://huggingface.co/openai/clip-vit-base-patch16">CLIP</a> model (ViT-B/16) pre-trained by OpenAI.
BioCAP achieves state-of-the-art performance on text-image retrieval tasks.</p>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#model-details" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="model-details">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Model Details
	</span>
</h2>
<h3 class="relative group flex items-center">
	<a rel="nofollow" href="#model-description" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="model-description">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Model Description
	</span>
</h3>
<p>Foundation models trained on large-scale biological data can benefit from richer multimodal supervision beyond taxonomic labels.
BioCAP extends <a rel="nofollow" href="https://imageomics.github.io/bioclip/">BioCLIP</a> by incorporating fine-grained synthetic captions and introducing dual visual projectors to better align images with both taxonomic and descriptive signals.
Trained on the <a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M">TreeOfLife-10M</a> dataset augmented with trait-focused synthetic captions (<a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M-Captions">TreeOfLife-10M-Captions</a>), BioCAP achieves significant improvements across multiple biological tasks.
Compared with <a rel="nofollow" href="https://imageomics.github.io/bioclip/">BioCLIP</a>, BioCAP improves zero-shot species classification by 8.8% and biological text-image retrieval by 21.3%, demonstrating the effectiveness of integrating descriptive, biologically grounded captions as complementary supervision for fine-grained multimodal learning.</p>
<ul>
<li><strong>Developed by:</strong> Ziheng Zhang, Xinyue Ma, Arpita Chowdhury, Elizabeth G Campolongo, Matthew J Thompson, Net Zhang, Samuel Stevens, Hilmar Lapp, Tanya Berger-Wolf, Yu Su, Wei-Lun Chao, Jianyang Gu</li>
<li><strong>Model type:</strong> The model uses a ViT-B/16 Transformer as an image encoder and uses a masked self-attention Transformer as a text encoder.</li>
<li><strong>License:</strong> MIT</li>
<li><strong>Fine-tuned from model:</strong> OpenAI CLIP, ViT-B/16 (<a rel="nofollow" href="https://huggingface.co/openai/clip-vit-base-patch16">Model weight</a>)</li>
</ul>
<h3 class="relative group flex items-center">
	<a rel="nofollow" href="#model-sources" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="model-sources">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Model Sources
	</span>
</h3>
<ul>
<li><strong>Homepage:</strong> <a rel="nofollow" href="https://imageomics.github.io/biocap">https://imageomics.github.io/biocap</a></li>
<li><strong>Repository:</strong> <a rel="nofollow" href="https://github.com/Imageomics/biocap">BioCAP</a></li>
<li><strong>Paper:</strong> <a rel="nofollow" href="https://arxiv.org/abs/2510.20095">BioCAP: Exploiting synthetic captions beyond labels in biological foundation models</a></li>
<li><strong>Demo:</strong> <a rel="nofollow" href="">BioCAP</a></li>
</ul>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#uses" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="uses">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Uses
	</span>
</h2>
<h3 class="relative group flex items-center">
	<a rel="nofollow" href="#direct-use" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="direct-use">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Direct Use
	</span>
</h3>
<p>The model can be used for zero-shot classification given species names.
It can also be applied to text–image retrieval, aligning biological images with descriptive queries. Additionally, it can support other language-related tasks that require grounding biological images in natural language.</p>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#bias-risks-and-limitations" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="bias-risks-and-limitations">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Bias, Risks, and Limitations
	</span>
</h2>
<p>BioCAP is trained on images from the <a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M">TreeOfLife-10M</a> dataset, which exhibits a long-tailed distribution across taxa. As a result, the predictions of BioCAP may be biased toward well-represented species. </p>
<p>BioCAP and <a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M">TreeOfLife-10M</a> paired with <a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M-Captions">TreeOfLife-10M-Captions</a> provide strong potential to support biodiversity research and conservation, especially by facilitating recognition and monitoring of species at scale.
However, as with many open-source tools, there are potential risks if misused. For example, improved recognition of rare or threatened species could theoretically aid poachers. At the same time, these same capabilities can serve as a force multiplier for conservation, enabling more effective monitoring of illicit trade and improving protection efforts.</p>
<p>Importantly, the dataset used to train BioCAP does not include geo-tagged location data, thereby reducing risks of misuse related to disclosing precise species habitats.</p>


<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#how-to-get-started-with-the-model" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="how-to-get-started-with-the-model">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		How to Get Started with the Model
	</span>
</h2>
<p>You can use the <code>open_clip</code> library to load BioCAP.</p>
<pre><code>import open_clip
model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms('hf-hub:imageomics/biocap')
tokenizer = open_clip.get_tokenizer('hf-hub:imageomics/biocap')
</code></pre>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#training-details" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="training-details">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Training Details
	</span>
</h2>
<h3 class="relative group flex items-center">
	<a rel="nofollow" href="#training-data" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="training-data">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Training Data
	</span>
</h3>
<p>This model was trained on <a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M">TreeOfLife-10M</a>, which is a compilation of images matched to <a rel="nofollow" href="https://www.britannica.com/science/taxonomy/The-objectives-of-biological-classification">Linnaean taxonomic rank</a> from kingdom through species. They are also matched with common (vernacular) name of the subject of the image where available. In addition, we augment the dataset with fine-grained synthetic captions (<a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M-Captions">TreeOfLife-10M-Captions</a>), automatically generated from domain-specific contexts (Wikipedia-derived traits and taxon-tailored format examples) to provide descriptive, biologically grounded supervision. For more information, please see our dataset, <a rel="nofollow" href="https://huggingface.co/datasets/imageomics/TreeOfLife-10M-Captions">TreeOfLife-10M-Captions</a>.</p>
<h3 class="relative group flex items-center">
	<a rel="nofollow" href="#training-procedure" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="training-procedure">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Training Procedure
	</span>
</h3>
<h4 class="relative group flex items-center">
	<a rel="nofollow" href="#preprocessing" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="preprocessing">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Preprocessing
	</span>
</h4>
<p>Standard CLIP image preprocessing is adopted in the training.</p>
<h4 class="relative group flex items-center">
	<a rel="nofollow" href="#training-hyperparameters" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="training-hyperparameters">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Training Hyperparameters
	</span>
</h4>
<ul>
<li><strong>Training regime:</strong> bf16 mixed precision </li>
</ul>
<p>We used an Adam optimizer with a maximum learning rate of 1e-4. 500 warming steps were adopted, followed by cosine decay.
The batch size of images was 4,096 per GPU.
We trained the model on 8 GPUs for 50 epochs, with a weight decay of 0.2.
Each input image was resized to 224 x 224 resolution.</p>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#evaluation" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="evaluation">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Evaluation
	</span>
</h2>
<p>We evaluated the model on zero-shot species classification, text–image retrieval, and <a rel="nofollow" href="https://inquire-benchmark.github.io">INQUIRE-rerank</a>.</p>
<h3 class="relative group flex items-center">
	<a rel="nofollow" href="#testing-data" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="testing-data">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Testing Data
	</span>
</h3>
<p>For species classification tasks, we tested BioCAP on the following 10 tasks:</p>
<ul>
<li><a rel="nofollow" href="https://dl.allaboutbirds.org/nabirds">NABirds</a>: We used 555 visual categories of 48,640 images for test.</li>
<li><a rel="nofollow" href="https://meta-album.github.io/">Meta-Album</a>: We used the Plankton, Insects, Insects2, PlantNet, Fungi, PlantVillage, and Medicinal Leaf datasets from Meta-Album. </li>
<li><a rel="nofollow" href="https://huggingface.co/datasets/imageomics/IDLE-OO-Camera-Traps">IDLE-OO Camera Traps</a>: Species identification in camera trap images is a real-world scenario that BioCAP can be applied to.
This dataset contains a class-balanced test sets from five LILA-BC camera trap datasets. For more information on this test set, please visit the <a rel="nofollow" href="https://huggingface.co/datasets/imageomics/IDLE-OO-Camera-Traps">dataset page</a>.</li>
<li><a rel="nofollow" href="https://huggingface.co/datasets/imageomics/rare-species">Rare Species</a>: This dataset was introduced in the first BioCLIP paper.
It consists of 400 species labeled Near Threatened through Extinct in the Wild by the <a rel="nofollow" href="https://www.iucnredlist.org/">IUCN Red List</a>, with 30 images per species.
Top-1 accuracy is reported for both zero-shot and few-shot experiments.</li>
</ul>
<p>For text-image retrieval tasks, we used:</p>
<ul>
<li><a rel="nofollow" href="https://inquire-benchmark.github.io">INQUIRE</a>: A benchmark designed to assess fine-grained retrieval and reranking performance. We used the rerank protocol, where the model must reorder 100 initially retrieved candidate images per query so that relevant ones are ranked higher.</li>
<li><a rel="nofollow" href="https://www.birds.cornell.edu/home/">Cornell Bird</a>: A paired image–text dataset we collected from the <a rel="nofollow" href="https://www.macaulaylibrary.org">Macaulay Library</a>. It contains naturalistic bird photographs paired with descriptive text.</li>
<li><a rel="nofollow" href="https://plantid.net/Home.aspx">PlantID</a>: A paired dataset we collected from <a rel="nofollow" href="https://plantid.net/Home.aspx">PlantID</a>. It provides plant photographs and associated textual descriptions for evaluating retrieval in botanical domains.</li>
</ul>
<p><strong>Note:</strong> More details regarding the evaluation implementation can be referred to in the <a rel="nofollow" href="https://arxiv.org/abs/2510.20095">paper</a>. Dataset access code and the CSVs for the last two text-image retrieval tasks are provided in the <a rel="nofollow" href="https://github.com/Imageomics/biocap/blob/main/BioCAP-pipeline.md#evaluation-data">evaluation section of the BioCAP Pipeline</a>.</p>
<h3 class="relative group flex items-center">
	<a rel="nofollow" href="#results" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="results">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Results
	</span>
</h3>
<p>We show the zero-shot classification and text-image retrieval task results here. For more detailed results, please check the <a rel="nofollow" href="https://arxiv.org/abs/2510.20095">paper</a>.</p>
<table cellspacing="0" cellpadding="0">
  <thead>
    <tr>
      <th rowspan="2">Model</th>
      <th colspan="5">Animals</th>
      <th colspan="4">Plants &amp; Fungi</th>
      <th rowspan="2">Rare Species</th>
      <th rowspan="2">Mean</th>
    </tr>
    <tr>
      <th>NABirds</th>
      <th>Plankton</th>
      <th>Insects</th>
      <th>Insects 2</th>
      <th>Camera Trap</th>
      <th>PlantNet</th>
      <th>Fungi</th>
      <th>PlantVillage</th>
      <th>Med. Leaf</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CLIP (ViT-B/16)</td>
      <td>39.0</td>
      <td>3.3</td>
      <td>7.4</td>
      <td>9.3</td>
      <td>28.1</td>
      <td>52.5</td>
      <td>8.6</td>
      <td>5.1</td>
      <td>15.0</td>
      <td>25.7</td>
      <td>19.4</td>
    </tr>
    <tr>
      <td>SigLIP</td>
      <td>50.2</td>
      <td>3.7</td>
      <td>17.6</td>
      <td>9.6</td>
      <td>26.7</td>
      <td>76.3</td>
      <td>28.3</td>
      <td>26.1</td>
      <td>45.4</td>
      <td>30.7</td>
      <td>32.3</td>
    </tr>
    <tr>
      <td>FG-CLIP</td>
      <td>48.3</td>
      <td>1.9</td>
      <td>6.9</td>
      <td>9.3</td>
      <td>26.4</td>
      <td>55.6</td>
      <td>7.3</td>
      <td>5.9</td>
      <td>15.7</td>
      <td>29.4</td>
      <td>20.7</td>
    </tr>
    <tr>
      <td>BioTrove-CLIP</td>
      <td>39.4</td>
      <td>1.0</td>
      <td>20.5</td>
      <td>15.7</td>
      <td>10.7</td>
      <td>64.4</td>
      <td>38.2</td>
      <td>15.7</td>
      <td>31.6</td>
      <td>24.6</td>
      <td>26.2</td>
    </tr>
    <tr>
      <td>BioCLIP</td>
      <td>58.8</td>
      <td>6.1</td>
      <td>34.9</td>
      <td>20.5</td>
      <td>31.7</td>
      <td>88.2</td>
      <td>40.9</td>
      <td>19.0</td>
      <td>38.5</td>
      <td>37.1</td>
      <td>37.6</td>
    </tr>
    <tr>
      <td><b>BioCAP (Ours)</b></td>
      <td><b>67.6</b></td>
      <td><b>7.2</b></td>
      <td><b>41.9</b></td>
      <td><b>23.7</b></td>
      <td><b>37.4</b></td>
      <td><b>93.6</b></td>
      <td><b>64.4</b></td>
      <td><b>33.0</b></td>
      <td><b>51.4</b></td>
      <td><b>44.2</b></td>
      <td><b>46.4</b></td>
    </tr>
  </tbody>
</table>

<table cellspacing="0" cellpadding="0">
  <thead>
    <tr>
      <th rowspan="2">Model</th>
      <th colspan="4">INQUIRE Rerank</th>
      <th colspan="2">Cornell Bird</th>
      <th colspan="2">PlantID</th>
      <th rowspan="2">Mean</th>
    </tr>
    <tr>
      <th>Appear.</th>
      <th>Behav.</th>
      <th>Context</th>
      <th>Species</th>
      <th>I2T</th>
      <th>T2I</th>
      <th>I2T</th>
      <th>T2I</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CLIP (ViT-B/16)</td>
      <td>30.8</td>
      <td>32.9</td>
      <td>37.2</td>
      <td>37.1</td>
      <td>33.8</td>
      <td>29.1</td>
      <td>25.0</td>
      <td>22.1</td>
      <td>31.0</td>
    </tr>
    <tr>
      <td>SigLIP</td>
      <td>34.6</td>
      <td><b>37.2</b></td>
      <td><b>41.4</b></td>
      <td>36.2</td>
      <td>47.7</td>
      <td>50.2</td>
      <td>42.1</td>
      <td>38.1</td>
      <td>40.9</td>
    </tr>
    <tr>
      <td>FG-CLIP</td>
      <td>28.8</td>
      <td>31.1</td>
      <td>32.5</td>
      <td>41.0</td>
      <td>49.4</td>
      <td>48.1</td>
      <td>28.7</td>
      <td>27.4</td>
      <td>35.9</td>
    </tr>
    <tr>
      <td>BioTrove-CLIP</td>
      <td>28.5</td>
      <td>22.2</td>
      <td>30.5</td>
      <td>39.5</td>
      <td>16.5</td>
      <td>13.8</td>
      <td>47.4</td>
      <td>50.1</td>
      <td>31.1</td>
    </tr>
    <tr>
      <td>BioCLIP</td>
      <td>27.4</td>
      <td>27.2</td>
      <td>30.8</td>
      <td>41.1</td>
      <td>15.1</td>
      <td>16.2</td>
      <td>47.8</td>
      <td>45.0</td>
      <td>31.3</td>
    </tr>
    <tr>
      <td><b>BioCAP (Ours)</b></td>
      <td><b>37.1</b></td>
      <td>33.6</td>
      <td>37.0</td>
      <td><b>43.0</b></td>
      <td><b>54.0</b></td>
      <td><b>52.0</b></td>
      <td><b>81.4</b></td>
      <td><b>83.0</b></td>
      <td><b>52.6</b></td>
    </tr>
  </tbody>
</table>


<h4 class="relative group flex items-center">
	<a rel="nofollow" href="#summary" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="summary">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Summary
	</span>
</h4>
<p>BioCAP surpasses BioCLIP by 8.8% on zero-shot species classification benchmarks.
Although the model is primarily trained to align images with taxonomic labels and synthetic captions, it also achieves strong performance on tasks beyond species classification.
Notably, BioCAP outperforms BioCLIP by 21.3% on biological text–image retrieval, demonstrating its effectiveness as a multimodal foundation model for biology.</p>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#technical-specifications" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="technical-specifications">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Technical Specifications
	</span>
</h2>
<h3 class="relative group flex items-center">
	<a rel="nofollow" href="#compute-infrastructure" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="compute-infrastructure">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Compute Infrastructure
	</span>
</h3>
<p>The training was performed on 8 NVIDIA H100-80GB GPUs distributed over 2 nodes on the <a rel="nofollow" href="https://www.osc.edu">Ohio Supercomputing Center</a>'s Cardinal Cluster.
It took 30hrs to complete the training of 50 epochs.</p>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#citation" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="citation">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Citation
	</span>
</h2>
<p><strong>Model:</strong></p>
<pre><code>@software{Zhang_BioCAP_model,
  author = {Ziheng Zhang and Xinyue Ma and Arpita Chowdhury and Elizabeth G Campolongo and Matthew J Thompson and Net Zhang and Samuel Stevens and Hilmar Lapp and Tanya Berger-Wolf and Yu Su and Wei-Lun Chao and Jianyang Gu},
  license = {MIT},
  title = {{BioCAP} (Revision af8db7a)},
  url = {https://huggingface.co/imageomics/biocap},
  version = {1.0.0},
  doi = {10.57967/hf/6799},
  publisher = {Hugging Face},
  year = {2025}
}
</code></pre>
<p>Please also cite our paper:</p>
<pre><code>@article{zhang2025biocap,
  title    = {Bio{CAP}: Exploiting Synthetic Captions Beyond Labels in Biological Foundation Models},
  author   = {Ziheng Zhang and Xinyue Ma and Arpita Chowdhury and Elizabeth G Campolongo and Matthew J Thompson and Net Zhang and Samuel Stevens and Hilmar Lapp and Tanya Berger-Wolf and Yu Su and Wei-Lun Chao and Jianyang Gu},
  year     = {2025},
  eprint   = {2510.20095},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2510.20095}
}
</code></pre>
<p>Also consider citing OpenCLIP and BioCLIP:</p>
<pre><code>@software{ilharco_gabriel_2021_5143773,
  author={Ilharco, Gabriel and Wortsman, Mitchell and Wightman, Ross and Gordon, Cade and Carlini, Nicholas and Taori, Rohan and Dave, Achal and Shankar, Vaishaal and Namkoong, Hongseok and Miller, John and Hajishirzi, Hannaneh and Farhadi, Ali and Schmidt, Ludwig},
  title={OpenCLIP},
  year={2021},
  doi={10.5281/zenodo.5143773},
}
</code></pre>
<p>Original BioCLIP Model:</p>
<pre><code>@software{bioclip2023,
  author = {Samuel Stevens and Jiaman Wu and Matthew J. Thompson and Elizabeth G. Campolongo and Chan Hee Song and David Edward Carlyn and Li Dong and Wasila M. Dahdul and Charles Stewart and Tanya Berger-Wolf and Wei-Lun Chao and Yu Su},
  doi = {10.57967/hf/1511},
  month = nov,
  title = {BioCLIP},
  version = {v0.1},
  year = {2023}
}
</code></pre>
<p>Original BioCLIP Paper:</p>
<pre><code>@inproceedings{stevens2024bioclip,
  title = {{B}io{CLIP}: A Vision Foundation Model for the Tree of Life}, 
  author = {Samuel Stevens and Jiaman Wu and Matthew J Thompson and Elizabeth G Campolongo and Chan Hee Song and David Edward Carlyn and Li Dong and Wasila M Dahdul and Charles Stewart and Tanya Berger-Wolf and Wei-Lun Chao and Yu Su},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2024},
  pages = {19412-19424}
}
</code></pre>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#acknowledgements" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="acknowledgements">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Acknowledgements
	</span>
</h2>
<p>We would like to thank Wasila Dahdul, Zhiyuan Tao, Yifan Liu, Fangxun Liu, Shuheng Wang, Ziqi Li, David Carlyn, Quang-Huy Nguyen, Yintie Lei, and Junke Yang for their help with the human evaluation, and the <a rel="nofollow" href="https://imageomics.osu.edu/about/team">Imageomics Team</a> for their constructive feedback.</p>
<p>We also gratefully acknowledge the use of paired text–image data from <a rel="nofollow" href="https://plantid.net/Home.aspx">PlantID</a> and the <a rel="nofollow" href="https://www.macaulaylibrary.org">Cornell Bird Macaulay Library</a> for retrieval evaluation.</p>
<p>This work was supported by the <a rel="nofollow" href="https://imageomics.org">Imageomics Institute</a>, which is funded by the US National Science Foundation's Harnessing the Data Revolution (HDR) program under <a rel="nofollow" href="https://www.nsf.gov/awardsearch/showAward?AWD_ID=2118240">Award #2118240</a> (Imageomics: A New Frontier of Biological Information Powered by Knowledge-Guided Machine Learning).</p>
<p>Our research is also supported by resources from the <a rel="nofollow" href="https://ror.org/01apna436">Ohio Supercomputer Center</a>.</p>
<p>Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.</p>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#model-card-authors" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="model-card-authors">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Model Card Authors
	</span>
</h2>
<p>Ziheng Zhang</p>
<h2 class="relative group flex items-center">
	<a rel="nofollow" href="#model-card-contact" class="block pr-1.5 text-lg md:absolute md:p-1.5 md:opacity-0 md:group-hover:opacity-100 md:right-full" id="model-card-contact">
		<span class="header-link"><svg viewBox="0 0 256 256" preserveAspectRatio="xMidYMid meet" height="1em" width="1em" role="img" aria-hidden="true" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" class="text-gray-500 hover:text-black dark:hover:text-gray-200 w-4"><path fill="currentColor" d="M167.594 88.393a8.001 8.001 0 0 1 0 11.314l-67.882 67.882a8 8 0 1 1-11.314-11.315l67.882-67.881a8.003 8.003 0 0 1 11.314 0zm-28.287 84.86l-28.284 28.284a40 40 0 0 1-56.567-56.567l28.284-28.284a8 8 0 0 0-11.315-11.315l-28.284 28.284a56 56 0 0 0 79.196 79.197l28.285-28.285a8 8 0 1 0-11.315-11.314zM212.852 43.14a56.002 56.002 0 0 0-79.196 0l-28.284 28.284a8 8 0 1 0 11.314 11.314l28.284-28.284a40 40 0 0 1 56.568 56.567l-28.285 28.285a8 8 0 0 0 11.315 11.314l28.284-28.284a56.065 56.065 0 0 0 0-79.196z"></path></svg></span>
	</a>
	<span>
		Model Card Contact
	</span>
</h2>
<p><a rel="nofollow" href="mailto:zhang.13617@osu.edu">zhang.13617@osu.edu</a></p>
<!-- HTML_TAG_END --></div>

				</div></section></div></main>

	</div>
		<script>
			 import("\/front\/build\/kube-08e8472\/index.js"); window.moonSha = "kube-08e8472\/"; window.__hf_deferred =
			{};
		</script>
		<!-- Stripe -->
		<script>
			if (["hf.co", "huggingface.co"].includes(window.location.hostname)) {
				const script = document.createElement("script");
				script.src = "https://js.stripe.com/v3/";
				script.async = true;
				document.head.appendChild(script);
			}
		</script>
	</body>
</html>

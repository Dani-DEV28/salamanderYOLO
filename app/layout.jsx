import Header from "@/app/components/Header"
import Footer from "@/app/components/Footer"
import FectchComp from "@/app/components/FetchComp"
import "@/app/globals.css"

export default function RootLayout({ children }) {
    return (
        <html>
            <body className="app-container">
                <Header />
                <FectchComp />
                <main className="app-content">
                    {children}
                </main>
                <Footer />
            </body>
        </html>
    )
}
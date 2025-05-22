'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import MainContainer from "@/components/main-container";
import { login } from "@/services/auth";
import { trainModel } from '@/services/model';

export default function LoginPage() {
    const router = useRouter();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async () => {
        await login(email, password);

        const must_train_model = await trainModel();

        if (must_train_model) {
            router.push('/set-database');

        }

        else {
            router.push('/chat');
        }

    };

    const handleSignUp = (e: React.MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();

        router.push('/sign-up');
    };

    return (
        <MainContainer>
            <div className="relative flex min-h-screen w-full overflow-hidden">
                {/* TODO: imagem de fundo não esta aparecendo */}
                <div className="absolute inset-0 -z-10">
                    <img
                        src="/background.jpg"
                        alt="Background"
                        className="w-full h-full object-cover opacity-10"
                    />
                </div>

                <div className="flex w-full">

                    <div className="w-1/2 flex flex-col items-center justify-center p-8">
                        <h2 className="text-3xl font-semibold text-purple-600 mb-6">Sign in</h2>

                        <div className="w-full max-w-md space-y-4">
                            <input
                                type="text"
                                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                                placeholder="Email"
                                onChange={(e) => setEmail(e.target.value)}
                            />

                            <input
                                type="password"
                                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                                placeholder="Password"
                                onChange={(e) => setPassword(e.target.value)}
                            />

                            <div className="h-4" />

                            <button className="w-full py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700" onClick={handleLogin}>
                                Login
                            </button>

                            <div className="text-center mt-4">
                                <p className="text-gray-600">
                                    Don't have an account?{' '}
                                    <a href="#" onClick={handleSignUp} className="text-purple-600 hover:underline">
                                        Sign up here
                                    </a>
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="w-1/2 relative">
                        <img
                            src="/chatbot_logo.png"
                            alt="Imagem de exemplo"
                            className="absolute bottom-4 right-4 w-1/5 pr-10 pb-4"
                        />
                    </div>
                </div>
            </div>
        </MainContainer>
    );
}